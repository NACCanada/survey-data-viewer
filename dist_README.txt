===============================================================================
                    📊 Survey Data Viewer v3.0
===============================================================================

Thank you for using Survey Data Viewer!

🚀 QUICK START
===============================================================================

1. Double-click "SurveyDataViewer.exe"
2. Your browser will open automatically to http://localhost:8080
3. Upload your CSV, Excel, or SPSS files and start analyzing!

💾 YOUR DATA
===============================================================================

All your surveys and data are stored in the "data" folder next to this exe.

📁 SurveyDataViewer.exe
📁 data/               ← Your surveys are here
📁 uploads/            ← Temporary upload folder

⚠️  IMPORTANT: Keep the "data" folder if you move the exe to preserve your surveys!

📋 FEATURES
===============================================================================

✓ Upload CSV, Excel (.xlsx), and SPSS (.sav) files
✓ Quick Filter Grid - filter data 10x faster
✓ Interactive charts and visualizations
✓ Cross-question analysis
✓ Multi-scenario comparison
✓ Export filtered data
✓ Crosstab/banner table viewer

🎯 QUICK FILTER TIPS
===============================================================================

• Quick Mode (default): See all demographics in a grid - check boxes and analyze!
• Advanced Mode: One-by-one filters with duplicate, bulk actions, comparisons
• Toggle modes: Click the mode buttons at the top of the filter section

🛠️ ADVANCED SETTINGS
===============================================================================

Change Port (if 8080 is already in use):
  1. Create a file named ".env" next to the exe
  2. Add this line: PORT=9000
  3. Restart the exe

Set Password Protection:
  1. In .env file add: SITE_PASSWORD=yourpassword
  2. Restart the exe
  3. You'll be prompted to login

🐛 TROUBLESHOOTING
===============================================================================

Browser doesn't open?
  → Manually visit http://localhost:8080

"Port already in use" error?
  → Change the port (see Advanced Settings above)
  → Or close other applications using port 8080

Can't upload files?
  → Make sure you have write permission in this folder
  → Check your antivirus isn't blocking it

Charts not showing?
  → Make sure JavaScript is enabled in your browser
  → Try a different browser (Chrome, Firefox, Edge)

🛑 STOPPING THE APPLICATION
===============================================================================

• Press Ctrl+C in the console window
• Or simply close the console window
• Or close your browser and the console

⚙️ SYSTEM REQUIREMENTS
===============================================================================

• Windows 7 or later (Windows 10/11 recommended)
• 4GB RAM minimum (8GB recommended for large datasets)
• 500MB free disk space
• Modern web browser (Chrome, Firefox, Edge)

📚 DOCUMENTATION
===============================================================================

Full documentation is available at:
https://github.com/yourrepo/nac-data-tool

Or check the docs/ folder if included with this distribution.

🔒 PRIVACY & DATA SECURITY
===============================================================================

• All data processing happens locally on YOUR computer
• No data is sent to the internet
• No tracking or analytics
• Your data never leaves your machine

💡 TIPS FOR BEST RESULTS
===============================================================================

• Use CSV or Excel files with clear column headers
• Keep datasets under 10,000 rows for best performance
• Close unused surveys to save memory
• Backup your "data" folder regularly

📧 SUPPORT
===============================================================================

For help, issues, or feature requests:
• Email: support@yourorganization.com
• GitHub: https://github.com/yourrepo/nac-data-tool/issues
• Documentation: See docs folder or visit the website

===============================================================================

Thank you for using Survey Data Viewer! 🎉

Built with Flask, Python, and PyInstaller
Version 3.0 | January 2025

===============================================================================
