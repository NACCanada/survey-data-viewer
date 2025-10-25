import os
import json
import uuid
import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import pandas as pd
import pyreadstat
from dotenv import load_dotenv
from crosstab_parser import CrosstabParser

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['DATA_FOLDER'] = os.getenv('DATA_FOLDER', 'data')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls', 'sav'}
app.config['SITE_PASSWORD'] = os.getenv('SITE_PASSWORD', 'changeme')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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


def process_sav_file(filepath):
    """Process SPSS SAV file and return dataframe with metadata"""
    try:
        # Read SAV file with metadata
        df, meta = pyreadstat.read_sav(filepath)

        # Get variable labels (question text)
        variable_labels = meta.column_names_to_labels

        # Get value labels (response options)
        value_labels = meta.variable_value_labels

        # Clean column names
        df.columns = df.columns.str.strip()

        return df, variable_labels, value_labels
    except Exception as e:
        raise Exception(f"Error processing SAV file: {str(e)}")


def process_file(filepath, file_extension):
    """Process CSV or Excel file and return dataframe"""
    try:
        if file_extension == 'csv':
            df = pd.read_csv(filepath)
        elif file_extension == 'sav':
            # For SAV files, only return the dataframe (no metadata for standard view)
            df, _, _ = process_sav_file(filepath)
        else:  # xlsx or xls
            df = pd.read_excel(filepath)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Convert all data to string for consistency in JSON
        df = df.fillna('')

        return df
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['SITE_PASSWORD']:
            session['authenticated'] = True
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Incorrect password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
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
@login_required
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

        # Handle SAV files specially for cross-question analysis
        if file_extension == 'sav':
            # Process SAV file with full metadata
            df, variable_labels, value_labels = process_sav_file(filepath)

            # Save raw survey data with metadata as JSON
            data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")
            data = {
                'columns': df.columns.tolist(),
                'data': df.to_dict('records'),
                'variable_labels': variable_labels,
                'value_labels': value_labels,
                'file_type': 'raw_survey'
            }
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Save metadata to database
            conn = sqlite3.connect('data/surveys.db')
            c = conn.cursor()
            c.execute('INSERT INTO surveys VALUES (?, ?, ?, ?, ?, ?)',
                      (survey_id, filename, datetime.now().isoformat(),
                       json.dumps(df.columns.tolist()), len(df), 'raw_survey'))
            conn.commit()
            conn.close()

            return jsonify({'success': True, 'survey_id': survey_id, 'file_type': 'raw_survey'})

        # Detect file type for non-SAV files
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
@login_required
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
    elif file_type == 'raw_survey':
        # Redirect to cross-question analysis viewer
        return redirect(url_for('view_cross_question', survey_id=survey_id))

    survey_info = {
        'id': survey_id,
        'filename': result[0],
        'upload_date': result[1],
        'columns': json.loads(result[2]),
        'row_count': result[3]
    }

    return render_template('survey.html', survey=survey_info)

@app.route('/api/survey/<survey_id>/data')
@login_required
def get_survey_data(survey_id):
    """API endpoint to get survey data"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/delete/<survey_id>', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def get_crosstab_data(survey_id):
    """API endpoint to get crosstab data"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/api/crosstab/<survey_id>/questions')
@login_required
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
@login_required
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


# Cross-question analysis routes
@app.route('/cross-question/<survey_id>')
@login_required
def view_cross_question(survey_id):
    """View cross-question analysis for raw survey data"""
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
        'total_responses': result[2]
    }

    return render_template('cross_question.html', survey=survey_info)


def clean_question_label(label, col_id):
    """Clean up question labels for better readability"""
    import re

    if not label or label == col_id:
        # If no label or label is same as ID, return the ID
        return col_id

    # Remove common prefixes
    label = re.sub(r'^(Q\d+[._-]?\s*)', '', label, flags=re.IGNORECASE)
    label = re.sub(r'^(Question\s*\d+[._-]?\s*)', '', label, flags=re.IGNORECASE)
    label = re.sub(r'^(QN\d+[._-]?\s*)', '', label, flags=re.IGNORECASE)

    # Remove trailing dots/dashes
    label = re.sub(r'[._-]+$', '', label)

    # Clean up multiple spaces
    label = re.sub(r'\s+', ' ', label)

    # Trim whitespace
    label = label.strip()

    # If label is too short after cleaning, use original
    if len(label) < 3:
        return col_id

    return label


@app.route('/api/cross-question/<survey_id>/metadata')
@login_required
def get_cross_question_metadata(survey_id):
    """Get metadata for cross-question analysis (questions, labels, etc.)"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Common metadata column patterns to exclude (exact matches or starts/ends with)
    metadata_exact = ['id', 'hid', 'respondent_id', 'response_id', 'timestamp',
                      'start_time', 'end_time', 'duration', 'completion_status',
                      'source', 'device', 'weight', 'status', 'ip_address',
                      'location', 'consent']

    metadata_startswith = ['respondent', 'response_', 'timestamp_', 'date_', 'time_',
                           'duration_', 'completion_', 'weight_', 'status_',
                           'ip_', 'location_', 'start_', 'end_', 'consent_']

    # Build question list with labels and value options
    # Only include columns that have value labels (actual questions)
    questions = []
    for col in data['columns']:
        # Check if this column has value labels (indicating it's a question)
        has_values = col in data['value_labels'] and data['value_labels'][col]

        # Skip if it's likely a metadata column (exact match or starts with pattern)
        col_lower = col.lower()
        is_metadata = (col_lower in metadata_exact or
                      any(col_lower.startswith(pattern) for pattern in metadata_startswith))

        # Only include if it has value labels and isn't metadata
        if has_values and not is_metadata:
            label = data['variable_labels'].get(col, col)

            question = {
                'id': col,
                'label': label,
                'values': data['value_labels'].get(col, {}),
                'value_count': len(data['value_labels'].get(col, {}))
            }
            questions.append(question)

    return jsonify({
        'questions': questions,
        'total_responses': len(data['data'])
    })


@app.route('/api/cross-question/<survey_id>/analyze', methods=['POST'])
@login_required
def analyze_cross_question(survey_id):
    """Perform cross-question analysis with filters"""
    data_path = os.path.join(app.config['DATA_FOLDER'], f"{survey_id}.json")

    if not os.path.exists(data_path):
        return jsonify({'error': 'Survey not found'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        survey_data = json.load(f)

    # Get request parameters
    params = request.get_json()
    target_question = params.get('target_question')
    filters = params.get('filters', [])  # List of {question_id, values}

    # Convert to DataFrame for easier filtering
    df = pd.DataFrame(survey_data['data'])

    # Apply filters
    filtered_df = df.copy()
    for filter_item in filters:
        question_id = filter_item['question_id']
        values = filter_item['values']
        if question_id in filtered_df.columns and values:
            # Convert values to appropriate types for comparison
            filtered_df = filtered_df[filtered_df[question_id].isin(values)]

    # Get target question data
    if target_question not in filtered_df.columns:
        return jsonify({'error': 'Target question not found'}), 400

    # Calculate value counts for filtered data
    value_counts_filtered = filtered_df[target_question].value_counts().to_dict()

    # Calculate value counts for unfiltered data (for comparison)
    value_counts_unfiltered = df[target_question].value_counts().to_dict()

    # Get value labels for display
    value_labels_raw = survey_data['value_labels'].get(target_question, {})

    # Convert value_labels keys to handle type mismatches (int/float/string)
    value_labels = {}
    for k, v in value_labels_raw.items():
        # Store with multiple key types to handle any mismatch
        try:
            # Try as int
            value_labels[int(float(k))] = v
            # Try as float
            value_labels[float(k)] = v
            # Keep as string
            value_labels[str(k)] = v
            # Also store the original key
            value_labels[k] = v
        except (ValueError, TypeError):
            value_labels[k] = v

    # Build result with labels for filtered data
    results = []
    all_values = set(value_counts_filtered.keys()) | set(value_counts_unfiltered.keys())

    for value in all_values:
        filtered_count = value_counts_filtered.get(value, 0)
        unfiltered_count = value_counts_unfiltered.get(value, 0)

        # Try to find label with multiple type conversions
        label = None
        try_values = [value, str(value)]
        if not isinstance(value, str):
            try:
                try_values.append(int(value))
            except (ValueError, TypeError):
                pass
            try:
                try_values.append(float(value))
            except (ValueError, TypeError):
                pass

        for try_value in try_values:
            if try_value in value_labels:
                label = value_labels[try_value]
                break

        if not label:
            label = str(value)

        results.append({
            'value': value,
            'label': label,
            'count': int(filtered_count),
            'percentage': round((filtered_count / len(filtered_df)) * 100, 1) if len(filtered_df) > 0 else 0,
            'unfiltered_count': int(unfiltered_count),
            'unfiltered_percentage': round((unfiltered_count / len(df)) * 100, 1) if len(df) > 0 else 0
        })

    # Sort by value
    results.sort(key=lambda x: x['value'])

    return jsonify({
        'target_question': target_question,
        'target_label': survey_data['variable_labels'].get(target_question, target_question),
        'total_filtered': len(filtered_df),
        'total_original': len(df),
        'filters_applied': filters,
        'results': results
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
