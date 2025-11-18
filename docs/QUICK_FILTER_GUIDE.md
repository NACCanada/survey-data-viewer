# Quick Filter Grid - User Guide

**Version 3.0 | January 2025**

---

## 🎯 Overview

The Quick Filter Grid is a major UX improvement that makes creating filters **10x faster** than the traditional one-by-one approach. Instead of clicking "Add Filter" repeatedly, you can now see all demographic questions in a grid and check multiple values across different questions simultaneously.

---

## 🚀 Quick Start

### Using Quick Mode (Default)

1. **Select your target question** from the dropdown
2. **Check values in the grid** - all demographic questions are visible at once
3. **Click "Apply Filters & Analyze"** - Done!

**Example:**
- ✅ Check "25-34" in Age Group
- ✅ Check "Male" in Gender
- ✅ Check "East" in Region
- Click "Apply Filters & Analyze"

**Result:** Instant analysis filtered by all three criteria!

---

## 🎨 Two Modes

### ⚡ Quick Mode (Default)

**Best for:** 90% of filtering tasks

**Features:**
- Grid shows all questions with ≤20 options
- Scrollable grid (600px max height)
- All/None buttons for each question
- One-click analyze

**Workflow:**
1. Select target question
2. Check boxes in grid
3. Click "Apply Filters & Analyze"

---

### 🔧 Advanced Mode

**Best for:** Complex scenarios, duplicating filters, multi-scenario comparison

**Features:**
- Everything in Quick Mode PLUS:
- Collapsible Quick Filter Grid
- Traditional "Add Filter" button
- Duplicate Filter button
- Bulk action buttons (Select All, Deselect All, Invert)
- Multi-scenario comparison mode

**Workflow:**
1. Select target question
2. Option A: Use grid → "Add Selected to Filters"
3. Option B: Click "Add Filter" for manual creation
4. Duplicate/modify filters as needed
5. Enable Multi-Scenario mode for comparisons

---

## 🎮 Features Breakdown

### Quick Filter Grid

**Location:** Available in both Quick and Advanced modes

**What it does:**
- Shows all filterable questions (≤20 options) in a grid layout
- Questions sorted with demographics first (Age, Gender, Region, etc.)
- Scrollable to prevent excessive page scrolling

**Quick actions per question:**
- **All** button: Check all values
- **None** button: Uncheck all values

---

### Duplicate Filter (Advanced Mode)

**What it does:**
- Copies an existing filter with all selected values
- Perfect for comparing similar groups

**Example use case:**
```
Filter #1: Age = 25-34, Gender = Male
[Duplicate] → Filter #2: Age = 25-34, Gender = Male
Change Filter #2 to: Age = 35-44, Gender = Male
Enable Multi-Scenario → Compare both age groups side-by-side
```

---

### Bulk Actions (Advanced Mode)

Available on each individual filter:

- **✓ Select All**: Check all checkboxes for that question
- **✗ Deselect All**: Uncheck all checkboxes
- **⇄ Invert Selection**: Toggle all checkboxes (checked → unchecked, unchecked → checked)

**Example:**
```
Question: Region (10 options)
Current: East, West selected
Click "Invert" → Now: North, South, Central, etc. selected (everything except East/West)
```

---

### Collapsible Grid (Advanced Mode)

**Show/Hide Grid Button:**
- Click "▼ Show Grid" to expand
- Click "▲ Hide Grid" to collapse
- Grid auto-collapses after adding filters to keep page clean

---

## 📊 Workflow Examples

### Example 1: Simple Demographic Filter

**Task:** Analyze church roles for young males in urban areas

**Quick Mode:**
1. Target Question: "What is your role?"
2. Grid selections:
   - Age: ✅ 18-24, ✅ 25-34
   - Gender: ✅ Male
   - Location: ✅ Urban
3. Click "Apply Filters & Analyze"

**Result:** Chart shows role distribution for young urban males

---

### Example 2: Compare Multiple Age Groups

**Task:** Compare church attendance across different age groups

**Advanced Mode:**
1. Target Question: "How often do you attend?"
2. Click "Show Grid"
3. Select: Age = 18-24, click "Add Selected to Filters"
4. Click "📋 Duplicate" on Filter #1
5. Change duplicate to Age = 25-34
6. Repeat for 35-44, 45-54, etc.
7. Enable "Multi-Scenario Mode"
8. Name each scenario (e.g., "Young Adults", "Middle Age", "Seniors")
9. Click "Compare All Scenarios"

**Result:** Grouped bar chart comparing attendance across all age groups

---

### Example 3: Complex Inverted Filter

**Task:** Analyze everyone EXCEPT weekly attendees in the West region

**Advanced Mode:**
1. Target Question: "What is your satisfaction level?"
2. Click "Add Filter"
3. Select Question: "Attendance Frequency"
4. Click "✓ Select All"
5. Uncheck "Weekly"
6. Add Filter #2: Region
7. Click "✓ Select All"
8. Uncheck "West"
9. Click "Analyze"

**OR using Invert:**
1. Add Filter: Attendance = Weekly
2. Click "⇄ Invert Selection"
3. Add Filter: Region = West
4. Click "⇄ Invert Selection"
5. Click "Analyze"

**Result:** Shows satisfaction for non-weekly attendees outside the West

---

## 🎯 Tips & Tricks

### Speed Tips

1. **Use Quick Mode** for simple demographic filtering (fastest)
2. **Use "All" buttons** in grid to quickly select everything, then deselect a few
3. **Use Invert** when you want "everything except X"
4. **Duplicate filters** instead of re-creating similar ones

### Best Practices

1. **Start in Quick Mode** - switch to Advanced only when needed
2. **Name scenarios clearly** when using Multi-Scenario comparison
3. **Use grid for demographics** - they're always at the top
4. **Collapse grid** in Advanced mode to keep workspace clean
5. **Check filter count** - too many filters (>5) might over-segment your data

### Common Patterns

**Pattern 1: Age Brackets**
```
Use Duplicate to create filters for:
- 18-24
- 25-34
- 35-44
- 45-54
- 55+
Then compare in Multi-Scenario mode
```

**Pattern 2: Gender Comparison**
```
Grid: Select all demographics EXCEPT gender
Add to Filters
Duplicate
Change one to Male, one to Female
Multi-Scenario comparison
```

**Pattern 3: Regional Analysis**
```
Grid: Select Age + Gender
Add to Filters
Duplicate 5 times (one per region)
Change Region in each
Compare all regions
```

---

## 🔧 Technical Details

### Grid Population

- Shows questions with **≤20 unique values**
- Questions sorted with demographics first:
  - Priority: AGE_GROUP, AGE, REGION, GENDER, EDUCATION, IDENTITY
  - Then alphabetically
- Values sorted numerically if possible, otherwise alphabetically

### Grid Layout

- **CSS Grid**: `repeat(auto-fill, minmax(400px, 1fr))`
- **Max Height**: 600px (shows ~3 rows)
- **Scrollable**: Custom purple scrollbar
- **Responsive**: Adjusts columns based on screen width

### Filter Conversion

**Quick Mode → Analysis:**
- Grid selections grouped by question
- Sent directly to `/api/cross-question/<id>/analyze`

**Advanced Grid → Filter Items:**
- Each question becomes a separate filter item
- Filter items appear in traditional UI
- Can be modified, duplicated, removed individually

---

## 🐛 Troubleshooting

### "No filterable questions found"

**Cause:** All questions have >20 options

**Solution:** Use Advanced mode → "Add Filter" button to manually select questions

---

### Grid doesn't show my question

**Cause:** Question has >20 unique values (too many for grid)

**Solution:** Use Advanced mode → "Add Filter" to manually add that question

---

### Selections not appearing in results

**Check:**
1. Did you select a target question?
2. Did you click "Apply Filters & Analyze" (Quick mode)?
3. Did you click "Add Selected to Filters" (Advanced grid)?
4. Are your filter values valid for the dataset?

---

### Grid is too tall/short

**Modify:** Edit `cross_question.html` line 194
```css
max-height: 600px;  /* Change to your preference */
```

---

## 🚀 Keyboard Shortcuts

Currently none - future enhancement idea!

**Potential shortcuts:**
- `Ctrl+Enter`: Analyze
- `Ctrl+D`: Duplicate current filter
- `Ctrl+A`: Select all in focused question
- `Esc`: Clear all selections

---

## 📈 Performance Notes

- **Grid rendering:** Instant for questions with <50 total options
- **Filter application:** Client-side grouping, then server-side analysis
- **Recommended:** Keep total checked values under 100 for best performance
- **Tested with:** 121 questions, 1000+ rows - no issues

---

## 🔮 Future Enhancements

Planned features:

- [ ] **Filter Presets**: Save common filter combinations
- [ ] **Search in Grid**: Filter questions by keyword
- [ ] **Keyboard shortcuts**: Power-user navigation
- [ ] **Sticky header**: Keep question names visible while scrolling
- [ ] **Expand/Collapse All**: Toggle all questions at once
- [ ] **Recent filters**: Quick access to recently used filters
- [ ] **Export filter config**: Share filter setups with team

---

## 📚 Related Documentation

- **CODEBASE_SUMMARY.md**: Technical implementation details
- **CLAUDE.md**: Project overview and development history
- **FEATURES.md**: Complete feature list
- **COMPARISON_GUIDE.md**: Multi-scenario comparison guide

---

## 🆘 Support

For issues or feature requests:
1. Check this guide first
2. Review CODEBASE_SUMMARY.md for technical details
3. Submit issue to project repository

---

**Last Updated**: January 18, 2025
**Version**: 3.0
**Author**: Built with Claude (Anthropic)
