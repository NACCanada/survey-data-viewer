import os
import json
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from dotenv import load_dotenv
from crosstab_parser import CrosstabParser

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['DATA_FOLDER'] = os.getenv('DATA_FOLDER', 'data')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls'}

# Initialize database
def init_db():
    conn = sqlite3.connect('data/surveys.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS surveys
                 (id TEXT PRIMARY KEY,
                  filename TEXT NOT NULL,
                  upload_date TEXT NOT NULL,
                  columns TEXT NOT NULL,
                  row_count INTEGER NOT NULL,
                  file_type TEXT DEFAULT 'standard')''')

    # Add file_type column if it doesn't exist (for existing databases)
    c.execute("PRAGMA table_info(surveys)")
    columns = [col[1] for col in c.fetchall()]
    if 'file_type' not in columns:
        c.execute('ALTER TABLE surveys ADD COLUMN file_type TEXT DEFAULT "standard"')

    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def detect_file_type(filepath, file_extension):
    """Detect if file is standard survey data or crosstab format"""
    try:
        if file_extension == 'csv':
            df = pd.read_csv(filepath, header=None, nrows=20)
        else:
            # Check if it has multiple sheets (likely crosstab)
            xl_file = pd.ExcelFile(filepath)
            if len(xl_file.sheet_names) > 1:
                # Check for BANNER pattern
                if any('BANNER' in sheet.upper() for sheet in xl_file.sheet_names):
                    return 'crosstab'

            df = pd.read_excel(filepath, header=None, nrows=20)

        # Look for crosstab indicators in first 20 rows
        for idx, row in df.iterrows():
            row_text = ' '.join([str(x) for x in row if pd.notna(x)])
            # Check for question patterns like "Q1.", "Q2.", etc.
            if any(pattern in row_text for pattern in ['Q1.', 'Q2.', 'Q3.']):
                # Check for demographic headers
                if any(keyword in row_text for keyword in ['Region', 'Age', 'Gender']):
                    return 'crosstab'

        return 'standard'

    except Exception:
        return 'standard'  # Default to standard if detection fails


def process_file(filepath, file_extension):
    """Process CSV or Excel file and return dataframe"""
    try:
        if file_extension == 'csv':
            df = pd.read_csv(filepath)
        else:  # xlsx or xls
            df = pd.read_excel(filepath)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Convert all data to string for consistency in JSON
        df = df.fillna('')

        return df
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

@app.route('/')
def index():
    """Home page with upload form and list of surveys"""
    conn = sqlite3.connect('data/surveys.db')
    c = conn.cursor()
    c.execute('SELECT id, filename, upload_date, row_count, file_type FROM surveys ORDER BY upload_date DESC')
    surveys = [{'id': row[0], 'filename': row[1], 'upload_date': row[2], 'row_count': row[3],
                'file_type': row[4] if len(row) > 4 else 'standard'}
               for row in c.fetchall()]
    conn.close()

    return render_template('index.html', surveys=surveys)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only CSV and Excel files are allowed.'}), 400

    try:
        # Generate unique ID for this survey
        survey_id = str(uuid.uuid4())[:8]

        # Save uploaded file
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{survey_id}_{filename}")
        file.save(filepath)

        # Detect file type
        file_type = detect_file_type(filepath, file_extension)

        if file_type == 'crosstab':
            # Process as crosstab
            parser = CrosstabParser(filepath)
            data = parser.parse_all_sheets()

            # Save crosstab data as JSON
            data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Save metadata
            conn = sqlite3.connect('data/surveys.db')
            c = conn.cursor()
            c.execute('INSERT INTO surveys VALUES (?, ?, ?, ?, ?, ?)',
                      (survey_id, filename, datetime.now().isoformat(),
                       json.dumps([]), data['metadata']['total_questions'], 'crosstab'))
            conn.commit()
            conn.close()

        else:
            # Process as standard file
            df = process_file(filepath, file_extension)

            # Save data as JSON
            data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")
            data = {
                'columns': df.columns.tolist(),
                'data': df.to_dict('records')
            }
            with open(data_path, 'w') as f:
                json.dump(data, f)

            # Save metadata to database
            conn = sqlite3.connect('data/surveys.db')
            c = conn.cursor()
            c.execute('INSERT INTO surveys VALUES (?, ?, ?, ?, ?, ?)',
                      (survey_id, filename, datetime.now().isoformat(),
                       json.dumps(df.columns.tolist()), len(df), 'standard'))
            conn.commit()
            conn.close()

        return jsonify({'success': True, 'survey_id': survey_id, 'file_type': file_type})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/survey/<survey_id>')
def view_survey(survey_id):
    """View survey data with filters"""
    conn = sqlite3.connect('data/surveys.db')
    c = conn.cursor()
    c.execute('SELECT filename, upload_date, columns, row_count, file_type FROM surveys WHERE id = ?', (survey_id,))
    result = c.fetchone()
    conn.close()

    if not result:
        return "Survey not found", 404

    file_type = result[4] if len(result) > 4 else 'standard'

    if file_type == 'crosstab':
        # Redirect to crosstab viewer
        return redirect(url_for('view_crosstab', survey_id=survey_id))

    survey_info = {
        'id': survey_id,
        'filename': result[0],
        'upload_date': result[1],
        'columns': json.loads(result[2]),
        'row_count': result[3]
    }

    return render_template('survey.html', survey=survey_info)

@app.route('/api/survey/<survey_id>/data')
def get_survey_data(survey_id):
    """API endpoint to get survey data"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/delete/<survey_id>', methods=['POST'])
def delete_survey(survey_id):
    """Delete a survey"""
    try:
        # Delete from database
        conn = sqlite3.connect('data/surveys.db')
        c = conn.cursor()
        c.execute('DELETE FROM surveys WHERE id = ?', (survey_id,))
        conn.commit()
        conn.close()

        # Delete files
        data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")
        if os.path.exists(data_path):
            os.remove(data_path)

        # Delete uploaded file
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            if file.startswith(f"{survey_id}_"):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Crosstab routes
@app.route('/crosstab/<survey_id>')
def view_crosstab(survey_id):
    """View crosstab data"""
    conn = sqlite3.connect('data/surveys.db')
    c = conn.cursor()
    c.execute('SELECT filename, upload_date, row_count FROM surveys WHERE id = ?', (survey_id,))
    result = c.fetchone()
    conn.close()

    if not result:
        return "Survey not found", 404

    survey_info = {
        'id': survey_id,
        'filename': result[0],
        'upload_date': result[1],
        'total_questions': result[2]
    }

    return render_template('crosstab.html', survey=survey_info)


@app.route('/api/crosstab/<survey_id>/data')
def get_crosstab_data(survey_id):
    """API endpoint to get crosstab data"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/api/crosstab/<survey_id>/questions')
def get_crosstab_questions(survey_id):
    """Get list of all questions in crosstab"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract questions from first banner
    if data['banners']:
        first_banner = list(data['banners'].values())[0]
        questions = [{'id': q['id'], 'text': q['text']} for q in first_banner['questions']]
        return jsonify({'questions': questions})

    return jsonify({'questions': []})


@app.route('/api/crosstab/<survey_id>/question/<question_id>')
def get_crosstab_question(survey_id, question_id):
    """Get specific question data from all banners"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = {'question_id': question_id, 'banners': {}}

    for banner_name, banner_data in data['banners'].items():
        for question in banner_data['questions']:
            if question['id'] == question_id:
                result['banners'][banner_name] = {
                    'question': question,
                    'demographics': banner_data['demographics'],
                    'column_labels': banner_data['column_labels']
                }
                break

    if not result['banners']:
        return jsonify({'error': 'Question not found'}), 404

    return jsonify(result)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
