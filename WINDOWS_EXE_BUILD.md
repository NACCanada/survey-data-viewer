# Building Windows Executable (.exe)

This guide explains how to package Survey Data Viewer as a single Windows `.exe` file that can be distributed to users without requiring Python installation.

---

## 📋 Prerequisites

### On Windows (for building the .exe)

1. **Python 3.8+** installed
2. **All project dependencies** installed
3. **PyInstaller** installed

```bash
# Install all dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller
```

---

## 🔨 Building the Executable

### Option 1: Using the Spec File (Recommended)

```bash
# Navigate to project directory
cd nac-data-tool

# Build using the spec file
pyinstaller survey_viewer.spec
```

### Option 2: Command Line Build

```bash
pyinstaller --onefile --name SurveyDataViewer ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "app.py;." ^
    --add-data "crosstab_parser.py;." ^
    --hidden-import flask ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import pyreadstat ^
    --console ^
    launcher.py
```

**Note:** On Windows, use semicolon (`;`) as path separator. On Mac/Linux, use colon (`:`).

---

## 📦 Build Output

After building, you'll find:

```
dist/
└── SurveyDataViewer.exe   ← This is your distributable file!
```

The `build/` and `__pycache__/` directories are temporary and can be deleted.

---

## 🚀 Distributing the .exe

### What to Share

**Option A - Minimal** (just the exe):
```
SurveyDataViewer.exe
```

**Option B - With Instructions** (recommended):
```
SurveyDataViewer.exe
README.txt           ← Simple usage instructions
```

**Option C - Full Package**:
```
SurveyDataViewer.exe
README.txt
sample_data.csv      ← Example data file
user_guide.pdf       ← Documentation
```

---

## 👤 User Instructions

### How Users Run It

1. **Double-click** `SurveyDataViewer.exe`
2. **Browser opens automatically** (or visit http://localhost:8080)
3. **Upload and analyze data**
4. **Press Ctrl+C in console** to stop (or just close the window)

### What Happens on First Run

The exe will automatically create these folders in the same directory:
```
📁 Where SurveyDataViewer.exe is located/
├── SurveyDataViewer.exe
├── data/           ← Created automatically (database + JSON files)
└── uploads/        ← Created automatically (temporary uploads)
```

### Data Persistence

- All survey data is stored in the `data/` folder next to the exe
- Users can move the exe, but should move the `data/` folder with it to keep their surveys
- To backup data: Copy the entire `data/` folder

---

## ⚙️ Configuration

### Changing Default Port

Create a `.env` file next to the exe:

```env
PORT=9000
SECRET_KEY=your-secret-key
SITE_PASSWORD=your-password
MAX_CONTENT_LENGTH=33554432
```

Or set environment variables before running:
```bash
set PORT=9000
SurveyDataViewer.exe
```

### Disabling Console Window

Edit `survey_viewer.spec`:
```python
console=False,  # Change from True to False
```

Then rebuild. This will hide the console window (runs silently in background).

**Note:** If you disable the console, add a system tray icon or make sure users know how to stop the process (Task Manager).

---

## 🐛 Troubleshooting Build Issues

### "Module not found" errors

Add missing modules to `hiddenimports` in `survey_viewer.spec`:

```python
hiddenimports=[
    'flask',
    'pandas',
    'your_missing_module',  # Add here
],
```

### "File not found" errors for templates/static

Check the `datas` section in `survey_viewer.spec`:

```python
datas=[
    ('templates', 'templates'),
    ('static', 'static'),
    # Add more here if needed
],
```

### Build is too large (>100 MB)

PyInstaller includes many dependencies. To reduce size:

1. Use `--exclude-module` for unused packages
2. Remove unused dependencies from requirements.txt
3. Use UPX compression (already enabled in spec file)

### Database errors when running exe

The exe needs write permissions. Make sure:
- User has write access to the folder
- Antivirus isn't blocking file creation
- The exe isn't running from a protected folder (like Program Files)

---

## 🔐 Code Signing (Optional but Recommended)

Windows may show warnings for unsigned executables. To sign your exe:

1. **Get a code signing certificate** (from CA like DigiCert, Sectigo)
2. **Sign the exe** with signtool:

```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/SurveyDataViewer.exe
```

**Benefits:**
- ✅ No Windows SmartScreen warnings
- ✅ Shows your organization name
- ✅ Users trust it more

---

## 📊 Testing the Build

Before distributing, test on a clean Windows machine:

1. **Copy only** `SurveyDataViewer.exe` to a test folder
2. **Run the exe** - browser should open
3. **Upload a CSV file** - verify it works
4. **Close and reopen** - verify data persists
5. **Check data/uploads folders** - should be created automatically

---

## 🎯 Advanced: Creating an Installer

For professional distribution, create an installer using:

### Option 1: Inno Setup (Free)

Download: https://jrsoftware.org/isinfo.php

Example script (`installer.iss`):
```iss
[Setup]
AppName=Survey Data Viewer
AppVersion=3.0
DefaultDirName={pf}\SurveyDataViewer
DefaultGroupName=Survey Data Viewer
OutputDir=installer_output
OutputBaseFilename=SurveyDataViewer_Setup

[Files]
Source: "dist\SurveyDataViewer.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Survey Data Viewer"; Filename: "{app}\SurveyDataViewer.exe"
Name: "{commondesktop}\Survey Data Viewer"; Filename: "{app}\SurveyDataViewer.exe"
```

### Option 2: NSIS (Free)

Download: https://nsis.sourceforge.io/

### Option 3: Advanced Installer (Paid)

Commercial tool with GUI: https://www.advancedinstaller.com/

---

## 🔄 Updating the Application

When releasing a new version:

1. **Update version number** in `launcher.py`:
   ```python
   print("     📊 Survey Data Viewer v3.1")  # Change here
   ```

2. **Rebuild the exe**:
   ```bash
   pyinstaller survey_viewer.spec
   ```

3. **Test thoroughly**

4. **Distribute new exe** with version in filename:
   ```
   SurveyDataViewer_v3.1.exe
   ```

---

## 📝 Build Checklist

Before distributing:

- [ ] Build completes without errors
- [ ] Exe runs and opens browser
- [ ] File upload works
- [ ] Data analysis works
- [ ] Filters work (Quick and Advanced modes)
- [ ] Charts render correctly
- [ ] Data persists after restart
- [ ] Tested on clean Windows machine
- [ ] Version number is correct
- [ ] README/instructions included
- [ ] (Optional) Code signed

---

## 🆘 Support & Issues

### Common User Issues

**"Windows protected your PC" warning:**
- This is normal for unsigned executables
- Click "More info" → "Run anyway"
- Or get the exe code-signed

**"Port already in use" error:**
- Another app is using port 8080
- Set PORT=9000 in .env file
- Or stop the other app

**"Can't find templates" error:**
- Exe was built incorrectly
- Rebuild with correct datas in spec file

**Slow startup:**
- First run extracts files (5-10 seconds normal)
- Subsequent runs are faster
- Antivirus scanning can slow it down

---

## 📚 Additional Resources

- **PyInstaller Documentation**: https://pyinstaller.org/
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **Windows Code Signing**: https://docs.microsoft.com/en-us/windows/win32/seccrypto/using-signtool

---

## 🔧 File Reference

**Key files for building:**
- `launcher.py` - Entry point for the exe
- `app.py` - Flask application (modified for exe compatibility)
- `survey_viewer.spec` - PyInstaller configuration
- `requirements.txt` - Python dependencies

**Changes made for exe compatibility:**
- Added path detection for bundled resources
- Created launcher with browser auto-open
- Made data directories auto-create
- Used environment variables for configuration

---

## ✅ Version History

**v3.0** (January 2025)
- Initial Windows exe support
- Auto-browser launch
- Portable data storage
- Quick Filter Grid feature

---

**Built with ❤️ using PyInstaller**

For issues or questions about building the exe, check:
1. This guide
2. PyInstaller documentation
3. Project issues on GitHub
