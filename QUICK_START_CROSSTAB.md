# Crosstab Viewer - Quick Start

## 🚀 Start the App

```bash
cd /Users/adityashah/nac-data-tool
python3 app.py
```

Open browser: **http://localhost:8080**

---

## ✅ Your File is Ready!

Your Environics crosstab file has already been uploaded and parsed:
- **Survey ID:** 970b95c7
- **Total Questions:** 78
- **Banners:** 3
- **Status:** ✅ Ready to view

**Direct link:** http://localhost:8080/crosstab/970b95c7

---

## 📋 Quick Actions

### Upload Another Crosstab File
1. Go to home page
2. Click "Choose a file..."
3. Select Excel file
4. Click "Upload"
5. System auto-detects crosstab format
6. Click "View Data"

### Browse Questions
- **Search:** Type in the search box (left sidebar)
- **Navigate:** Click any question to view
- **Tip:** Questions are numbered Q2-Q79

### Compare Demographics

1. Select question from left sidebar
2. Scroll to "Demographic Comparison"
3. Choose first demographic (dropdown 1)
4. Choose second demographic (dropdown 2)
5. Chart appears automatically!

**Examples:**
- West vs ON (regions)
- Female vs Male (gender)
- 16-34 vs 70+ (age groups)
- University vs High school (education)

### Switch Banners

Click the banner tabs at the top:
- **BANNER 1** - Region, Age, Gender, Education, etc.
- **BANNER 2** - Different demographic cuts
- **BANNER 3** - Additional breakdowns

---

## 🎯 Key Features

| What | How | Where |
|------|-----|-------|
| Find question | Search box | Left sidebar |
| View details | Click question | Main area |
| See demographics | Look at table | Below question text |
| Compare groups | Select 2 demographics | Bottom of page |
| Switch view | Click banner tabs | Top of main area |

---

## 💡 Pro Tips

1. **Use search** - Faster than scrolling through 78 questions
2. **Try different banners** - Each has unique demographic breakdowns
3. **Compare related groups** - E.g., all age groups or all regions
4. **Look for patterns** - Large differences = interesting insights!

---

## 📊 Your Survey Data

- **Respondents:** 1,189
- **Questions:** 78
- **Question Topics:**
  - Service attendance
  - Church involvement
  - Ministry participation
  - Volunteer activities
  - Satisfaction levels
  - Demographics

---

## 🔧 Troubleshooting

**Server not starting?**
```bash
pip3 install Flask pandas openpyxl python-dotenv
```

**Page not loading?**
- Check server is running (terminal shows "Running on http://...")
- Try http://localhost:8080 (not https)
- Refresh browser

**No questions showing?**
- Wait a few seconds for data to load
- Check browser console (F12) for errors
- Verify survey ID in URL is correct

---

## 📁 Files Created

```
nac-data-tool/
├── crosstab_parser.py          # Parser for crosstab files
├── app.py                       # Updated with crosstab routes
├── templates/
│   └── crosstab.html           # Crosstab viewer interface
├── data/
│   └── 970b95c7.json           # Your parsed survey data
└── CROSSTAB_VIEWER_GUIDE.md    # Detailed documentation
```

---

## 🎉 You're All Set!

Your crosstab file is ready to explore. The viewer gives you:

✅ Easy question navigation
✅ Multiple demographic views
✅ Interactive comparisons
✅ Visual charts

**Start exploring:** http://localhost:8080/crosstab/970b95c7

---

## 📞 Need Help?

- **Full Guide:** See `CROSSTAB_VIEWER_GUIDE.md`
- **API Docs:** See endpoint examples in full guide
- **General Help:** See `README.md` and `FEATURES.md`
