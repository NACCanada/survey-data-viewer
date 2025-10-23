# Survey Data Format Guide

## What You Need to Request from Environics

Your current file (`Environics - New Apostolic Church - Member Survey - Detailed Tables October 2025.xlsx`) is in **crosstab/analysis format** - it shows aggregated statistics, not individual responses.

For the Survey Data Viewer to work, you need the **raw respondent-level data**.

---

## Current Format (What You Have)

**Type:** Crosstab / Detailed Tables / Banner Tables
**Structure:** Statistical analysis report

```
Question               | Total | West | ON  | East | Age 16-34 | Age 35-54 | ...
-----------------------|-------|------|-----|------|-----------|-----------|----
Q2: Service Attendance |       |      |     |      |           |           |
  Once a week          | 851   | 167  | 632 | 29   | 97        | 234       | ...
  % of total           | 71.5% | 71.4%| ... | ...  | ...       | ...       | ...
  2-3 times/month      | 197   | 27   | ... | ...  | ...       | ...       | ...
```

**Characteristics:**
- ✗ Questions as rows
- ✗ Demographics as columns
- ✗ Cells contain counts and percentages
- ✗ Includes statistical significance testing
- ✗ Multiple sheets with different demographic breakdowns

---

## Required Format (What You Need)

**Type:** Raw respondent-level data
**Structure:** One row per survey respondent

```
RespondentID | Region | Age   | Gender | Q2_Service_Attendance | Q3_Satisfaction | ...
-------------|--------|-------|--------|-----------------------|-----------------|----
1            | West   | 16-34 | Female | Once a week          | Very satisfied  | ...
2            | ON     | 35-54 | Male   | 2-3 times/month      | Somewhat sat.   | ...
3            | East   | 55-69 | Female | Once a month         | Very satisfied  | ...
4            | West   | 70+   | Male   | Never                | Neutral         | ...
...
```

**Characteristics:**
- ✓ Each row = one person's complete responses
- ✓ Each column = one question or demographic field
- ✓ Cells contain actual responses (not statistics)
- ✓ Can be filtered, sorted, and analyzed dynamically

---

## Example File Created

I've created **`sample_raw_survey_data.csv`** in this directory that shows exactly what format you need.

### The sample includes:

**Demographic Fields:**
- RespondentID (unique identifier)
- Region
- Age
- Gender
- Education
- Marital_Status
- Identity
- Tenure_in_Canada
- General_Happiness

**Survey Questions:**
- Q2_Service_Attendance
- Q3_Satisfaction_with_Church
- Q4_Years_as_Member
- Q5_Volunteer_Activities
- (... and all other questions from your survey)

---

## What to Ask Your Survey Provider

### Email Template to Environics:

```
Subject: Request for Raw Survey Data - NAC Member Survey October 2025

Hi [Contact Name],

Thank you for the detailed tables file. For our internal analysis tool,
we need the data in a different format.

Could you please provide the raw respondent-level data with:

1. One row per survey respondent
2. One column per question/demographic variable
3. Actual response values (not aggregated statistics)
4. CSV or Excel format

Specifically:
- Include the respondent ID (anonymized)
- Include all demographic variables as columns
- Include all survey questions (Q1, Q2, Q3, etc.) as columns
- Each cell should contain the actual response that person gave

We currently have the crosstab/banner tables, but need the underlying
raw data file that was used to generate those tables.

Please let me know if you have any questions.

Thank you!
```

---

## Format Requirements Checklist

When you receive the data file, verify it has:

- [ ] **One row per respondent** (not one row per question)
- [ ] **Column headers** with question names/IDs
- [ ] **Actual response values** (not percentages or counts)
- [ ] **All demographic fields** as separate columns
- [ ] **All survey questions** as separate columns
- [ ] **No merged cells** or complex formatting
- [ ] **CSV or Excel format** (.csv, .xlsx)
- [ ] **UTF-8 encoding** (for special characters)

---

## File Size Guidelines

Your crosstab shows approximately **1,189 total respondents**.

Expected raw data file:
- **Rows:** ~1,189 (one per person)
- **Columns:** 50-100+ (depending on number of questions)
- **File size:** 100KB - 2MB (very manageable)
- **Format:** CSV (preferred) or Excel (.xlsx)

---

## Testing with Sample Data

To test the Survey Data Viewer while waiting for the real data:

```bash
# Start the application
python app.py

# Upload the sample_raw_survey_data.csv file
# Test filtering, charts, and comparison features
```

The sample data has the exact structure your real data should have, just with:
- 50 respondents instead of 1,189
- Randomized responses for demonstration
- Subset of questions from your survey

---

## Why This Format is Better

The raw respondent-level format allows you to:

1. **Filter dynamically** - "Show me only women aged 35-54 in Ontario"
2. **Cross-tabulate on the fly** - Generate any demographic breakdown you want
3. **Compare groups** - Group A vs Group B with any criteria
4. **Export subsets** - Download filtered data for further analysis
5. **Generate charts** - Automatic visualization of any question
6. **Drill down** - See individual responses, not just aggregates

With crosstabs, you're limited to the pre-defined demographic breakdowns.
With raw data, you can analyze however you want!

---

## Questions?

If Environics asks why you need this format or has questions about the structure,
feel free to share this document or the sample CSV file as a reference.

Most survey providers have the raw data readily available - it's what they used
to generate the crosstabs you received.
