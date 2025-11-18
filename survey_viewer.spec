# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Survey Data Viewer
# Build with: pyinstaller survey_viewer.spec

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('app.py', '.'),
        ('crosstab_parser.py', '.'),
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'flask',
        'pandas',
        'openpyxl',
        'pyreadstat',
        'werkzeug',
        'jinja2',
        'click',
        'itsdangerous',
        'markupsafe',
        'numpy',
        'sqlalchemy',
        'email_validator',
        'crosstab_parser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SurveyDataViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add 'icon.ico' here if you have one
)
