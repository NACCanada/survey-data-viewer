# Survey Data Viewer - Codebase Summary
**Last Updated**: 2025-01-25

This document serves as a comprehensive reference to avoid re-analyzing the codebase. Read this file first in new sessions.

---

## 📁 Project Structure

```
nac-data-tool/
├── app.py                          # Main Flask application (650+ lines)
├── crosstab_parser.py              # Parses Environics-style banner/crosstab Excel files
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
├── data/                           # SQLite DB + JSON data storage
│   ├── surveys.db                  # Survey metadata database
│   └── {survey_id}.json           # Individual survey data files
├── uploads/                        # Temporary file uploads
├── templates/
│   ├── index.html                  # Home page with upload form
│   ├── survey.html                 # Standard survey viewer (CSV/Excel)
│   ├── crosstab.html              # Crosstab/banner viewer
│   └── cross_question.html        # Cross-question filtering & analysis
└── static/
    ├── css/style.css              # All styling
    └── js/
        ├── main.js                # Home page functionality
        └── survey.js              # Standard survey view logic
```

---

## 🗄️ Database Schema (SQLite)

**Table: surveys**
```sql
CREATE TABLE surveys (
    id TEXT PRIMARY KEY,              -- 8-char hex ID
    filename TEXT NOT NULL,           -- Original filename
    upload_date TEXT NOT NULL,        -- ISO timestamp
    total_responses INTEGER,          -- Number of rows
    file_type TEXT DEFAULT 'standard' -- 'standard', 'crosstab', or 'raw_survey'
);
```

**File Types:**
- `standard`: CSV/Excel with raw data → survey.html
- `crosstab`: Environics banner tables → crosstab.html
- `raw_survey`: SPSS .sav files → cross_question.html

---

## 🔌 API Endpoints

### Upload & View
| Method | Endpoint | Purpose | Returns |
|--------|----------|---------|---------|
| GET | `/` | Home page | HTML |
| POST | `/upload` | Upload CSV/Excel/SAV | Redirect to viewer |
| GET | `/survey/<id>` | Standard survey viewer | HTML |
| GET | `/crosstab/<id>` | Crosstab viewer | HTML |
| GET | `/cross-question/<id>` | Cross-question analysis | HTML |

### Data APIs
| Method | Endpoint | Purpose | Returns |
|--------|----------|---------|---------|
| GET | `/api/survey/<id>/data` | Get survey data | JSON with rows |
| GET | `/api/crosstab/<id>/data` | Get full crosstab | JSON with banners |
| GET | `/api/crosstab/<id>/questions` | List all questions | JSON array |
| GET | `/api/crosstab/<id>/question/<qid>` | Get question across all banners | JSON |
| GET | `/api/cross-question/<id>/metadata` | Get questions with labels | JSON |
| POST | `/api/cross-question/<id>/analyze` | Run filtered analysis | JSON with results |

---

## 🎯 Key Features & Implementation

### 1. Cross-Question Filtering (cross_question.html)
**File**: `templates/cross_question.html` (1470+ lines)

**Features:**
- Single-scenario mode: Traditional filtering
- Multi-scenario mode: Compare up to 6 filter combinations
- Natural sorting of questions (Q1, Q2... Q10, Q70)
- Demographics prioritized: Age, Region, Gender, Education, Identity

**How It Works:**
1. User selects target question
2. Adds filter scenarios with conditions
3. Click "Compare All Scenarios"
4. Backend runs analysis for each scenario (POST `/api/cross-question/<id>/analyze`)
5. Frontend displays grouped bar chart + comparison table

**Key Functions:**
- `toggleComparisonMode()`: Switch between single/multi mode
- `addScenario()`: Create new scenario card
- `compareAllScenarios()`: Run analysis for all scenarios
- `displayScenarioChart()`: Render Chart.js grouped bars
- `displayScenarioTable()`: Build comparison table

**Backend Logic** (`app.py:531-637`):
```python
# Filters questions to prioritize demographics
priority_fields = ['AGE_GROUP', 'AGE', 'REGION', 'GENDER', 'EDUCATION', 'IDENTITY']

# Natural sorting for Q1, Q2... Q10
def natural_sort_key(text):
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]

# Analysis endpoint applies filters sequentially
filtered_df = df.copy()
for filter_item in filters:
    filtered_df = filtered_df[filtered_df[question_id].isin(values)]
```

### 2. Crosstab Viewer (crosstab.html)
**File**: `templates/crosstab.html` (2055+ lines)

**Features:**
- View pre-aggregated banner tables
- Single question mode: View one question across demographics
- Cross-banner comparison mode: Compare same question across banners
- Cross-question cross-banner mode: Compare different questions with different banners
- Cascading demographic filters (up to 4 levels deep)

**How It Works:**
1. Upload Environics-style Excel file
2. `crosstab_parser.py` extracts banners, demographics, questions, responses
3. Saved as JSON structure with metadata
4. Frontend loads questions and displays with filters
5. Charts generated with Chart.js

**Key Functions:**
- `switchViewMode()`: Toggle single/comparison mode
- `toggleQuestionSelection()`: Select questions for comparison
- `updateQuestionFilter()`: Change banner/demographic per question
- `updateCrossQuestionDisplay()`: Generate comparison charts
- `renderCrossQuestionChart()`: Chart.js with custom tooltips

### 3. Crosstab Parser (crosstab_parser.py)
**Purpose**: Parse Environics-style Excel banner tables

**Key Methods:**
- `parse_all_sheets()`: Process all banners
- `parse_banner(sheet_name)`: Extract demographics, questions, responses
- `_find_demographic_headers()`: Locate column headers
- `_find_questions()`: Identify Q1., Q2., etc.
- `_parse_question_data()`: Extract values per demographic
- `export_to_json()`: Save parsed structure

**Output Structure:**
```json
{
  "metadata": { "filename": "...", "sheets": [...], "total_questions": 50 },
  "banners": {
    "BANNER 1": {
      "demographics": [
        {"category": "Region", "label": "East", "column_index": 2}
      ],
      "questions": [
        {
          "id": "Q1",
          "text": "Question text",
          "responses": [
            {"response": "Yes", "values": [45, 50, 38]}
          ]
        }
      ]
    }
  }
}
```

---

## 🔧 Common Modifications

### Adding a New Field to Priority List
**File**: `app.py:530`
```python
priority_fields = ['AGE_GROUP', 'AGE', 'REGION', 'GENDER', 'EDUCATION', 'IDENTITY']
# Add new field here
```

### Changing Metadata Exclusion Patterns
**File**: `app.py:496-503`
```python
metadata_exact = ['id', 'hid', 'respondent_id', ...]
metadata_startswith = ['respondent', 'response_', ...]
```
**Note**: Use exact match or startswith patterns to avoid false positives (e.g., "GENDER" was excluded because "id" appeared in "gen-d-er")

### Modifying Scenario Comparison Colors
**File**: `cross_question.html:1058`
```javascript
const colors = ['#667eea', '#f093fb', '#28a745', '#ffc107', '#dc3545', '#17a2b8'];
```

### Adjusting Max Scenarios
**File**: `cross_question.html:1225`
```javascript
if (activeScenarios.length === 0) {
    alert('Please add at least one scenario with filters');
    return;
}
// No hard limit currently, but UI supports up to 6 colors
```

---

## 📊 Data Flow

### Upload Flow
```
1. User uploads file → POST /upload
2. Detect file type:
   - Multiple sheets with "BANNER" → crosstab
   - .sav extension → raw_survey
   - Otherwise → standard
3. Process file:
   - Crosstab: Parse with crosstab_parser.py
   - SAV: Read with pyreadstat, extract labels
   - Standard: Read with pandas
4. Save to data/{id}.json
5. Insert metadata into surveys.db
6. Redirect to appropriate viewer
```

### Cross-Question Analysis Flow
```
1. GET /cross-question/<id> → Load page
2. JS: fetch /api/cross-question/<id>/metadata
   - Returns questions sorted with demographics first
3. User configures scenarios with filters
4. Click "Compare All Scenarios"
5. For each scenario:
   - POST /api/cross-question/<id>/analyze with filters
   - Backend filters DataFrame sequentially
   - Returns counts and percentages
6. JS: Aggregate results and render chart + table
```

### Crosstab Flow
```
1. GET /crosstab/<id> → Load page
2. JS: fetch /api/crosstab/<id>/data
   - Returns full parsed JSON structure
3. User selects questions and demographics
4. JS: Filter and display locally (no server calls)
5. Generate charts with Chart.js
```

---

## 🛠️ Technologies & Versions

**Backend:**
- Flask 3.0.0
- pandas 2.2.3
- openpyxl 3.1.2 (Excel read/write)
- pyreadstat 1.2.7 (SPSS .sav files)
- gunicorn 21.2.0 (production server)

**Frontend:**
- Vanilla JavaScript (no framework)
- jQuery 3.7.1
- DataTables 1.13.7
- Chart.js 4.4.0

**Database:**
- SQLite 3 (embedded)

---

## 🔐 Security Features

- ✅ Secure filename handling with werkzeug
- ✅ File type validation
- ✅ File size limits (16MB default)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Password authentication (configurable)
- ⚠️  No CSRF protection (add for production)
- ⚠️  No rate limiting (add for production)

---

## 🚀 Recent Changes (Jan 2025)

1. **Cross-Question Filtering Enhancement**
   - Added multi-scenario comparison mode
   - Compare up to 6 filter combinations on one chart
   - Scenario naming and management

2. **Cross-Banner Comparison**
   - Select different banners per question
   - Independent demographic selection
   - Color-coded comparison view

3. **Bug Fixes**
   - Fixed GENDER exclusion (metadata pattern matching)
   - Fixed question sorting (Q7 before Q70 → natural order)
   - White background for instructions section

4. **UI Improvements**
   - Demographic fields prioritized in dropdowns
   - Clear workflow instructions with examples
   - Better visual hierarchy

---

## 💡 Quick Reference

**Need to modify question sorting?**
→ `app.py:532-550` (natural_sort_key and sort_key functions)

**Need to change which fields appear first?**
→ `app.py:530` (priority_fields list)

**Need to modify scenario comparison?**
→ `cross_question.html:1037-1466` (multi-scenario functions)

**Need to parse different crosstab format?**
→ `crosstab_parser.py` (modify parsing logic)

**Need to add new file type support?**
→ `app.py:60-87` (detect_file_type function)

**Need to change authentication?**
→ `app.py:30-50` (login_required decorator)

---

## 📝 Testing Notes

**Tested with:**
- ✅ 1000+ row datasets
- ✅ SPSS .sav files with 121 variables
- ✅ Environics crosstab banners (5 sheets)
- ✅ CSV/Excel standard files
- ✅ Multiple demographics and filters

**Known Limitations:**
- Client-side rendering best for <10k rows per survey
- No pagination for very large datasets
- No async processing for large file uploads

---

**For Future Sessions:**
Read this file first to understand the codebase structure and avoid re-analyzing files!
