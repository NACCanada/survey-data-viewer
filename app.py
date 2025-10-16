import os
import json
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from dotenv import load_dotenv

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
                  row_count INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
    c.execute('SELECT id, filename, upload_date, row_count FROM surveys ORDER BY upload_date DESC')
    surveys = [{'id': row[0], 'filename': row[1], 'upload_date': row[2], 'row_count': row[3]}
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

        # Process file
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
        c.execute('INSERT INTO surveys VALUES (?, ?, ?, ?, ?)',
                  (survey_id, filename, datetime.now().isoformat(),
                   json.dumps(df.columns.tolist()), len(df)))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'survey_id': survey_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/survey/<survey_id>')
def view_survey(survey_id):
    """View survey data with filters"""
    conn = sqlite3.connect('data/surveys.db')
    c = conn.cursor()
    c.execute('SELECT filename, upload_date, columns, row_count FROM surveys WHERE id = ?', (survey_id,))
    result = c.fetchone()
    conn.close()

    if not result:
        return "Survey not found", 404

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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
