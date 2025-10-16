# Data Comparison Guide

The Survey Data Viewer now includes a powerful **Comparison Mode** that lets you compare two different segments of your data side-by-side.

---

## What is Comparison Mode?

Comparison Mode allows you to:
- Define two groups (Group A and Group B) using different filter criteria
- Compare distributions across these groups
- View side-by-side charts showing differences
- Analyze how different segments respond or behave

---

## How to Use Comparison Mode

### Step 1: Enable Comparison Mode

1. Navigate to your survey view page
2. Click the **"Compare Data"** button in the Filters section
3. The comparison interface will appear with two side-by-side panels

### Step 2: Define Your Groups

**Group A (Left Panel):**
- Set filters to define your first segment
- Example: Department = "Engineering"

**Group B (Right Panel):**
- Set filters to define your second segment
- Example: Department = "Marketing"

### Step 3: View Comparison Results

The comparison results section shows:
- **Group Counts**: How many records match each group's filters
- **Side-by-Side Charts**: Visual comparison of distributions for each column
- **Group A** shown in **blue**
- **Group B** shown in **red**

### Step 4: Close Comparison

Click **"Close Comparison"** to return to normal filtering mode

---

## Use Cases

### 1. Department Comparison
**Question**: How do Engineering and Sales departments differ in satisfaction?

**Steps**:
1. Group A: Department = "Engineering"
2. Group B: Department = "Sales"
3. Compare the "Satisfaction" chart

**Result**: See if one department is more satisfied than the other

---

### 2. Before/After Analysis
**Question**: Did satisfaction improve after a policy change?

**Steps**:
1. Group A: Survey Date = "2024-Q1"
2. Group B: Survey Date = "2024-Q2"
3. Compare satisfaction levels

**Result**: Visualize improvements or declines

---

### 3. Demographic Comparison
**Question**: Do different age groups have different preferences?

**Steps**:
1. Group A: Age = "18-30"
2. Group B: Age = "31-50"
3. Compare across all categorical columns

**Result**: Identify age-related patterns

---

### 4. Location Comparison
**Question**: How do regional offices compare?

**Steps**:
1. Group A: Location = "New York"
2. Group B: Location = "Los Angeles"
3. Compare responses

**Result**: See regional differences

---

### 5. Segment Analysis
**Question**: How do highly satisfied customers differ from dissatisfied ones?

**Steps**:
1. Group A: Satisfaction = "Very Satisfied"
2. Group B: Satisfaction = "Dissatisfied"
3. Compare other attributes (Department, Age, etc.)

**Result**: Understand what differentiates satisfied from dissatisfied respondents

---

## Features

### Multi-Filter Groups
- Each group can have multiple filters applied
- Example: Group A = Engineering + Very Satisfied
- Example: Group B = Sales + Neutral

### Real-Time Updates
- Charts update instantly as you change filters
- No need to click "Apply" or "Refresh"

### All Columns Compared
- Automatically generates comparison charts for all categorical columns
- Only shows columns with ≤20 unique values for clarity

### Count Display
- Shows exact count of records in each group
- Helps understand sample sizes

---

## Tips for Effective Comparisons

### 1. Balanced Groups
Try to compare groups of similar sizes for meaningful insights:
- ✅ Good: Group A = 45 records, Group B = 50 records
- ⚠️ Caution: Group A = 5 records, Group B = 200 records

### 2. Clear Definitions
Use specific, non-overlapping filters:
- ✅ Good: Group A = "Engineering", Group B = "Sales"
- ❌ Avoid: Group A = "All", Group B = "Engineering" (overlapping)

### 3. Meaningful Comparisons
Compare groups that have a reason to differ:
- ✅ Good: Before/After, Different locations, Different demographics
- ❌ Less useful: Random subsets with no logical connection

### 4. Check Sample Sizes
Small groups may show misleading patterns:
- Aim for at least 10-20 records per group
- Larger groups provide more reliable insights

### 5. Multiple Filters
Combine filters for specific segments:
- Example: Engineering + New York vs Engineering + LA
- Example: Q1 + Satisfied vs Q2 + Satisfied

---

## Reading Comparison Charts

### Bar Heights
- Taller bars = more records in that category
- Compare heights between blue (Group A) and red (Group B)

### Patterns to Look For
- **Similar Heights**: Groups behave similarly
- **Different Heights**: Key differences between groups
- **Missing Bars**: One group has zero in that category

### Example Interpretation

```
Satisfaction Chart:
Very Satisfied: Group A = 30, Group B = 15
Satisfied:      Group A = 10, Group B = 25
Neutral:        Group A = 5,  Group B = 10
```

**Interpretation**: Group A is more satisfied overall than Group B

---

## Limitations

1. **Categorical Data Only**: Charts only show columns with ≤20 unique values
2. **No Numeric Analysis**: Currently doesn't calculate averages or statistical significance
3. **Visual Comparison**: Based on chart visualization, not statistical tests
4. **Memory**: Large datasets may be slower to compare

---

## Advanced Workflows

### Workflow 1: Progressive Filtering
1. Start broad: Department comparison
2. Narrow down: Add satisfaction level to both groups
3. Refine: Add more filters to isolate specific segments

### Workflow 2: A/B Testing Results
1. Group A: Control group (feature disabled)
2. Group B: Test group (feature enabled)
3. Compare satisfaction, usage, feedback

### Workflow 3: Cohort Analysis
1. Define cohorts by time period
2. Compare early vs recent respondents
3. Track changes over time

### Workflow 4: Segmentation Study
1. Test multiple comparisons:
   - Engineering vs Sales
   - Engineering vs Marketing
   - Engineering vs HR
2. Identify which departments differ most
3. Focus analysis on significant differences

---

## Exporting Comparison Results

While in comparison mode, you can still:
1. Take screenshots of comparison charts
2. Use browser print function to save as PDF
3. Export filtered data from each group separately:
   - Set filters for Group A → Close comparison → Export
   - Set filters for Group B → Export
4. Combine exports in spreadsheet for analysis

---

## Future Enhancements

Planned features for comparison mode:
- Export comparison charts as images
- Statistical significance testing
- Percentage view alongside counts
- Three-group comparison
- Save/load comparison configurations
- Comparison report generation

---

## Troubleshooting

### Charts not showing?
- Ensure both groups have at least some data
- Check that columns have ≤20 unique values
- Try refreshing the page

### Groups showing 0 count?
- Filters may be too restrictive
- Try broadening filter criteria
- Check that filter values exist in data

### Comparison button not working?
- Ensure page fully loaded
- Check browser console for errors
- Try refreshing the page

---

## Keyboard Tips

- Use **Tab** to navigate between filter dropdowns
- Use **Arrow keys** to select options quickly
- **Escape** to close dropdown (browser default)

---

## Best Practices

1. **Start Simple**: Compare one dimension at a time
2. **Document Findings**: Take notes or screenshots
3. **Iterative Analysis**: Start broad, narrow down
4. **Context Matters**: Consider sample sizes and distributions
5. **Multiple Angles**: Try different comparison criteria

---

## Examples by Industry

### HR/Employee Surveys
- Compare departments
- Before/after policy changes
- Office locations
- Tenure groups (new vs veteran employees)

### Customer Feedback
- Product A vs Product B users
- New customers vs returning customers
- Different service tiers
- Geographic regions

### Academic Surveys
- Class A vs Class B
- Before/after intervention
- Different teaching methods
- Demographics (age, gender, major)

### Healthcare Surveys
- Treatment A vs Treatment B
- Pre-treatment vs post-treatment
- Different facilities
- Demographics

---

## Questions?

For additional help:
- Check README.md for general usage
- See FEATURES.md for full feature list
- Review sample_survey.csv for example data

Happy comparing! 📊
