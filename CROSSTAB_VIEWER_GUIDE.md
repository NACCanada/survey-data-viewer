# Crosstab Viewer Guide

## Overview

The Survey Data Viewer now supports **both** standard survey data (one row per respondent) **and** crosstab/detailed tables format (statistical analysis reports).

Your Environics file has been successfully integrated and is ready to use!

---

## What Was Built

### ✅ Features Implemented

1. **Automatic File Type Detection**
   - Uploads automatically detect whether files are standard data or crosstab format
   - Detection looks for:
     - Multiple sheets with "BANNER" in name
     - Question patterns (Q1., Q2., Q3., etc.)
     - Demographic headers (Region, Age, Gender, etc.)

2. **Crosstab Parser** (`crosstab_parser.py`)
   - Extracts all 78 questions from your survey
   - Parses 3 banners (BANNER 1, 2, 3) with different demographic breakdowns
   - Identifies 20+ demographic groups per banner
   - Preserves all response data and values

3. **Interactive Crosstab Viewer**
   - Question navigation sidebar with search
   - Browse all 78 questions easily
   - Switch between 3 banners for different demographic views
   - Side-by-side demographic comparison with charts

4. **Visualization Features**
   - Demographic comparison charts
   - Select any two demographics to compare (e.g., West vs ON, or Age 16-34 vs 35-54)
   - Grouped bar charts showing response patterns
   - Real-time updates

---

## How to Use

### 1. Start the Application

```bash
cd /Users/adityashah/nac-data-tool
python3 app.py
```

The server will start at http://localhost:8080

### 2. Access Your Crosstab Data

Your Environics file has already been uploaded! Visit:

```
http://localhost:8080/
```

You'll see your survey listed with a **CROSSTAB** badge.

### 3. View Crosstab Data

Click "View Data" on your survey card, or go directly to:

```
http://localhost:8080/crosstab/970b95c7
```

### 4. Navigate Questions

**Question Sidebar (Left):**
- Browse all 78 questions
- Use the search box to find specific questions
- Click any question to view details

**Main Content Area (Right):**
- View full question text
- See demographic breakdowns in a table
- Switch between BANNER 1, 2, and 3

### 5. Compare Demographics

**To compare two demographic groups:**

1. Scroll to "Demographic Comparison" section
2. Select first demographic (e.g., "West")
3. Select second demographic (e.g., "ON")
4. Chart appears automatically showing side-by-side comparison

**Examples:**
- Compare regions: West vs ON vs East/North
- Compare age groups: 16-34 vs 35-54 vs 55-69 vs 70+
- Compare genders: Female vs Male
- Compare education levels
- Compare marital status groups

---

## Understanding Your Data

### Your Survey Structure

- **Total Questions:** 78
- **Banners:** 3 (different demographic breakdowns)
- **Demographics per Banner:** ~20 groups
- **Sample Size:** 1,189 respondents

### BANNER 1 Demographics

1. Region: West, ON, East/North
2. Age: 16-34, 35-54, 55-69, 70+
3. Gender: Female, Male
4. Education: High school or less, Apprenticeship/College, University
5. Marital Status: Single, Married/common law, Divorced/widowed
6. Identity: White, Racialized and Indigenous
7. Tenure in Canada: < 10 years, 10+ years, Born in Canada

### Sample Questions

- Q2: How often do you usually attend service at our church?
- Q3: How long have you been attending our church?
- Q5: Are you a minister at our church?
- Q7: Do you volunteer at our church?
- Q10-Q13: Agreement/disagreement statements
- And 68 more questions...

---

## Technical Details

### File Detection

When you upload an Excel file, the system checks:

```python
# Checks for BANNER sheets
if any('BANNER' in sheet.upper() for sheet in xl_file.sheet_names):
    return 'crosstab'

# Checks for question patterns
if any(pattern in row_text for pattern in ['Q1.', 'Q2.', 'Q3.']):
    if any(keyword in row_text for keyword in ['Region', 'Age', 'Gender']):
        return 'crosstab'
```

### Data Structure

Parsed data is stored as JSON:

```json
{
  "metadata": {
    "total_questions": 78,
    "sheets": ["BANNER 1", "BANNER 2", "BANNER 3"]
  },
  "banners": {
    "BANNER 1": {
      "demographics": [
        {"category": "Region", "label": "West", "column_index": 2},
        {"category": "Region", "label": "ON", "column_index": 3},
        ...
      ],
      "questions": [
        {
          "id": "Q2",
          "text": "Q2. How often do you usually attend service...",
          "responses": [
            {
              "response": "At least once a week",
              "values": [851.0, 167.0, 632.0, ...]
            },
            ...
          ]
        }
      ]
    }
  }
}
```

### API Endpoints

1. **List all questions:**
   ```
   GET /api/crosstab/{survey_id}/questions
   ```

2. **Get specific question:**
   ```
   GET /api/crosstab/{survey_id}/question/{question_id}
   ```

3. **Get all crosstab data:**
   ```
   GET /api/crosstab/{survey_id}/data
   ```

---

## Features by User Request

### You Asked For:
1. ✅ **Browse questions with search/filter** - Implemented in left sidebar
2. ✅ **Compare demographics side-by-side** - Implemented with Chart.js visualizations

### Additional Features (Not Requested):
- Banner tab switching (view all 3 banners for each question)
- Statistics summary cards (total questions, banners, current question)
- Full response data tables
- Responsive design
- Real-time chart updates

---

## Differences from Standard Viewer

| Feature | Standard Viewer | Crosstab Viewer |
|---------|----------------|-----------------|
| Data Format | One row per person | Aggregated statistics |
| Filtering | Dynamic row-level filters | Fixed demographic segments |
| Comparison | Custom group filters | Pre-defined demographic groups |
| Charts | Auto-generated per column | Demographic comparison charts |
| Export | Filter and export rows | View and analyze tables |
| Use Case | Explore individual responses | Analyze demographic patterns |

---

## Workflow Tips

### Exploring Your Survey

1. **Start with overview:**
   - Look at the 3 stat cards at the top
   - See total questions and banners available

2. **Browse questions:**
   - Use search to find topics (e.g., "volunteer", "attend", "minister")
   - Click through questions sequentially
   - Review response distributions in the table

3. **Analyze demographics:**
   - Switch banners to see different demographic cuts
   - Use comparison tool for specific group analysis
   - Look for patterns across age, region, education, etc.

4. **Deep dive:**
   - Focus on questions with interesting patterns
   - Compare multiple demographic pairs
   - Note significant differences between groups

---

## Next Steps

### If You Want More Features

Additional capabilities that could be added:

1. **Export functionality:**
   - Export specific questions to CSV
   - Export comparison charts as images
   - Generate PDF reports

2. **Advanced comparisons:**
   - Compare 3+ demographics simultaneously
   - Overlay multiple questions
   - Show percentage vs absolute values toggle

3. **Statistical analysis:**
   - Highlight statistically significant differences
   - Show confidence intervals
   - Calculate effect sizes

4. **Custom views:**
   - Save favorite question sets
   - Create custom dashboards
   - Bookmark specific comparisons

Let me know if you'd like any of these additions!

---

## Troubleshooting

### "Survey not found"
- Check that the survey ID in the URL is correct
- Verify the file was uploaded successfully

### "No questions found"
- The parser may not have detected questions correctly
- Check that the file has the expected format
- Look at the console output for parsing errors

### Charts not appearing
- Ensure two different demographics are selected
- Check browser console for JavaScript errors
- Verify Chart.js is loading correctly

### Performance issues
- The crosstab viewer loads all data at once
- For very large surveys, consider limiting to one banner at a time
- Close other browser tabs if experiencing slowness

---

## File Location

Your crosstab data is stored at:

```
/Users/adityashah/nac-data-tool/data/970b95c7.json
```

This JSON file contains all parsed data and can be:
- Backed up for safekeeping
- Shared with team members
- Used in other analysis tools
- Re-uploaded if needed

---

## Summary

✅ **Your Environics file now works with the Survey Data Viewer!**

The crosstab viewer provides:
- Easy question navigation
- Multiple demographic breakdowns
- Interactive comparisons
- Visual analytics

You can upload additional crosstab files the same way, and the system will automatically detect and parse them correctly.

Enjoy exploring your survey data!
