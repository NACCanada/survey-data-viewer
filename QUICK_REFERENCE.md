# Quick Reference Guide

Ultra-concise reference for common modifications. For detailed info, see CODEBASE_SUMMARY.md.

---

## 📍 File Locations

| Feature | File | Lines |
|---------|------|-------|
| Cross-Question Filtering | `templates/cross_question.html` | 1-1470 |
| Crosstab Viewer | `templates/crosstab.html` | 1-2055 |
| Flask API Routes | `app.py` | 1-660 |
| Crosstab Parser | `crosstab_parser.py` | 1-400 |

---

## 🎯 Common Tasks

### Add New Priority Field
```python
# File: app.py, Line: 530
priority_fields = ['AGE_GROUP', 'AGE', 'REGION', 'GENDER', 'EDUCATION', 'IDENTITY']
# Add new field here ↑
```

### Change Question Sorting
```python
# File: app.py, Lines: 532-550
def natural_sort_key(text):
    # Modify sorting logic here
```

### Fix Metadata Filtering
```python
# File: app.py, Lines: 496-503
metadata_exact = ['id', 'hid', ...]
metadata_startswith = ['respondent', 'response_', ...]
```

### Modify Scenario Colors
```javascript
// File: cross_question.html, Line: 1058
const colors = ['#667eea', '#f093fb', '#28a745', '#ffc107', '#dc3545', '#17a2b8'];
```

### Change Max File Size
```python
# File: app.py, Line: 20
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

---

## 🔌 Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/upload` | POST | Upload file |
| `/api/cross-question/<id>/metadata` | GET | Get question list |
| `/api/cross-question/<id>/analyze` | POST | Run filtered analysis |
| `/api/crosstab/<id>/data` | GET | Get crosstab data |

---

## 🗂️ Data Storage

- **Database**: `data/surveys.db` (SQLite)
- **Survey Data**: `data/{survey_id}.json` (JSON files)
- **Uploads**: `uploads/` (temporary)

---

## 🐛 Common Issues & Fixes

### Question sorting wrong (Q10 before Q2)
**Fix**: Natural sorting already implemented in `app.py:532-550`

### GENDER field missing
**Fix**: Check metadata patterns in `app.py:496-503` - avoid substring matches

### Scenario colors not showing
**Fix**: Check `cross_question.html:1058` - max 6 colors defined

### Upload fails for large files
**Fix**: Increase `MAX_CONTENT_LENGTH` in `app.py:20`

---

## 🔧 File Type Detection

```python
# File: app.py, Lines: 60-87
# Crosstab: Multiple sheets with "BANNER" in names
# Raw Survey: .sav extension
# Standard: Everything else
```

---

## 📊 Feature Flags

Current features can be toggled via UI:
- **Cross-Question**: Multi-scenario mode checkbox
- **Crosstab**: View mode toggle (single/comparison)

No server-side feature flags currently implemented.

---

**Read CODEBASE_SUMMARY.md for detailed explanations!**
