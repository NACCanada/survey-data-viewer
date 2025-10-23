# Format Comparison: Crosstab vs Raw Data

## Side-by-Side Comparison

### Your Current File (Crosstab Format) ❌

```
Q2. How often do you usually attend service at our church?

                        | TOTAL | West | ON  | East | 16-34 | 35-54 | Female | Male |
------------------------|-------|------|-----|------|-------|-------|--------|------|
Total                   | 1189  | 234  | 861 | 58   | 164   | 355   | 658    | 488  |
NET: Attendee           | 1109  | 209  | 812 | 54   | 141   | 324   | 607    | 466  |
  % of total            | 93.3% | 89.3%| 94.3| 93.1 | 86.0  | 91.3  | 92.2   | 95.5 |
NET: Regular Attendee   | 1048  | 194  | 772 | 50   | 127   | 302   | 579    | 436  |
  % of total            | 88.1% | 82.9%| 89.7| 86.2 | 77.4  | 85.1  | 88.0   | 89.3 |
At least once a week    | 851   | 167  | 632 | 29   | 97    | 234   | 457    | 370  |
  % of total            | 71.6% | 71.4%| 73.4| 50.0 | 59.1  | 65.9  | 69.5   | 75.8 |
2-3 times a month       | 197   | 27   | 140 | 21   | 30    | 68    | 122    | 66   |
  % of total            | 16.6% | 11.5%| 16.3| 36.2 | 18.3  | 19.2  | 18.5   | 13.5 |
Once a month            | 61    | 15   | 40  | 4    | 14    | 22    | 31     | 34   |
...
```

**Problems for Dynamic Analysis:**
- ❌ Can't filter by multiple criteria (e.g., "Women aged 35-54 in West region")
- ❌ Can't create new demographic breakdowns
- ❌ Can't see individual responses
- ❌ Can't export filtered data
- ❌ Static - limited to pre-calculated combinations

---

### Required Format (Raw Data) ✅

```
RespondentID | Region | Age   | Gender | Education    | Q2_Service_Attendance | Q3_Satisfaction | Q4_Years_Member | ...
-------------|--------|-------|--------|--------------|-----------------------|-----------------|-----------------|----
1            | West   | 16-34 | Female | University   | Once a week          | Very satisfied  | 5               | ...
2            | ON     | 35-54 | Male   | College      | 2-3 times/month      | Somewhat sat.   | 12              | ...
3            | East   | 55-69 | Female | High school  | Once a month         | Very satisfied  | 25              | ...
4            | West   | 70+   | Male   | University   | Never                | Neutral         | 3               | ...
5            | ON     | 16-34 | Female | College      | Once a week          | Very satisfied  | 8               | ...
6            | ON     | 35-54 | Female | University   | 2-3 times/month      | Very satisfied  | 15              | ...
...
(continues for all 1,189 respondents)
```

**Advantages for Dynamic Analysis:**
- ✅ Filter by any combination (e.g., "Female, 35-54, West, University educated")
- ✅ Create any demographic breakdown you want
- ✅ Compare any two groups (Group A vs Group B)
- ✅ Export filtered subsets for deeper analysis
- ✅ Generate charts for any question
- ✅ See individual response patterns
- ✅ Dynamic - unlimited analysis possibilities

---

## Real-World Example

### Question: "What % of women aged 35-54 in Ontario attend weekly?"

**With Crosstab (Current File):**
```
Step 1: Find the "Age 35-54" column → 234 people attend weekly (65.9% of all 35-54)
Step 2: Find the "Female" column → 457 people attend weekly (69.5% of all females)
Step 3: Find the "ON" column → 632 people attend weekly (73.4% of all ON)

Result: ??? - Can't combine these three criteria!
You'd need a different crosstab with that exact demographic breakdown.
```

**With Raw Data (What You Need):**
```
Step 1: Filter where Region = "ON" AND Age = "35-54" AND Gender = "Female"
Step 2: Count how many have Q2_Service_Attendance = "Once a week"
Step 3: Calculate percentage

Result: Instant answer! (e.g., "42 out of 85 = 49.4%")
```

---

## How the Survey Data Viewer Works

### With Raw Data (One Row Per Person):

**Upload the file** → Instant features:

1. **Dynamic Filters**
   - Select: Region = "ON", Age = "35-54", Gender = "Female"
   - Table updates instantly showing only those 85 people
   - All their complete responses are visible

2. **Automatic Charts**
   - Bar chart for Q2 (Service Attendance) appears
   - Shows distribution for your filtered subset
   - Updates in real-time as you change filters

3. **Comparison Mode**
   - Group A: Women aged 35-54 in Ontario
   - Group B: Men aged 35-54 in Ontario
   - Side-by-side charts comparing attendance patterns

4. **Export**
   - Download CSV of just those 85 filtered people
   - Use in Excel, SPSS, or other tools

---

## What Your Survey Provider Has

Environics **definitely has** your raw data file! Here's their workflow:

```
Step 1: Collect survey responses
        ↓
Step 2: Create raw data file (1,189 rows × ~50-100 columns)
        ← YOU NEED THIS FILE
        ↓
Step 3: Import into SPSS/statistical software
        ↓
Step 4: Run crosstab analyses
        ↓
Step 5: Export to Excel with banners/detailed tables
        ↓
Step 6: Send you the crosstab file
        ← THIS IS WHAT YOU CURRENTLY HAVE
```

You just need to ask them to send you the **Step 2 file** instead of (or in addition to) the Step 6 file.

---

## File Size Comparison

### Your Current Crosstab File:
- 3+ sheets (BANNER 1, 2, 3)
- 3,454+ rows (questions × response options × statistics)
- 22+ columns (demographic breakdowns)
- Complex merged cells and formatting
- File size: ~500KB - 2MB

### Raw Data File (What You Need):
- 1 sheet
- 1,189 rows (one per respondent)
- ~50-100 columns (all questions + demographics)
- Simple tabular format
- File size: ~100KB - 500KB

**The raw data file is actually smaller and simpler!**

---

## Quick Reference Table

| Feature | Crosstab (Current) | Raw Data (Needed) |
|---------|-------------------|-------------------|
| One row per... | Question/statistic | Person |
| Filter by multiple demographics | ❌ Limited | ✅ Unlimited |
| Create custom breakdowns | ❌ No | ✅ Yes |
| See individual responses | ❌ No | ✅ Yes |
| Export filtered data | ❌ No | ✅ Yes |
| Generate new charts | ❌ Static | ✅ Dynamic |
| Compare custom groups | ❌ No | ✅ Yes |
| File size | Larger | Smaller |
| Complexity | High | Low |
| Analysis flexibility | Low | High |

---

## Next Steps

1. **Use the email template** in `DATA_FORMAT_GUIDE.md` to contact Environics
2. **Share the sample file** (`sample_raw_survey_data.csv`) as a reference
3. **Request the raw data export** - they likely have this ready to go
4. **Test with sample data** while waiting (use the sample file I created)

The raw data format is:
- Simpler to work with
- More flexible for analysis
- Standard industry format
- What the Survey Data Viewer was designed for

You'll be able to do **much more analysis** with the raw data than with the crosstabs!
