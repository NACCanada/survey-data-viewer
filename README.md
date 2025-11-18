# Survey Data Viewer

A lightweight web application for uploading, visualizing, and filtering CSV and Excel survey data.

## ⭐ What's New in v3.0 (January 2025)

**🚀 Quick Filter Grid** - Filter creation just got 10x faster!

- **Quick Mode**: See all demographics in a grid, check values, analyze - done in seconds
- **Enhanced Advanced Mode**: Duplicate filters, bulk actions (Select All/None/Invert), collapsible grid
- **Smart Grid**: Shows only filterable questions (≤20 options), scrollable to reduce page height
- **Power Features**: All/None buttons per question, automatic demographic prioritization

[📖 Read the Quick Filter Guide](docs/QUICK_FILTER_GUIDE.md) | [🎯 Try it now!](#installation)

---

## Features

### Core Features
- Upload CSV, Excel, and SPSS (.sav) files
- Automatic page generation for each upload
- **NEW: Quick Filter Grid** for rapid demographic filtering
- Dynamic filters based on column headers with bulk actions
- Sortable and searchable data tables
- Interactive charts with Chart.js
- Export filtered data to CSV or JSON
- Cross-question analysis with multi-scenario comparison
- Crosstab/banner table viewer
- Responsive design
- Easy deployment with Docker

### Advanced Features
- **Quick Filter Mode**: Grid-based multi-select for all demographics
- **Duplicate Filter**: Copy existing filters with one click
- **Bulk Actions**: Select All, Deselect All, Invert Selection
- **Multi-Scenario Comparison**: Compare up to 6 filter combinations side-by-side
- **Natural Sorting**: Questions sorted intelligently (Q1, Q2...Q10, not Q1, Q10, Q2)
- **Demographic Priority**: Age, Gender, Region always appear first

## Installation

### 🪟 Windows - Single .exe File (Easiest!)

**For Windows users who want zero setup:**

1. Download `SurveyDataViewer.exe` from releases
2. Double-click to run - that's it!
3. Browser opens automatically at http://localhost:8080

No Python installation needed! All data stored next to the exe.

[📦 Download Windows .exe](#) | [📖 Build Your Own](WINDOWS_EXE_BUILD.md)

---

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

2. Access the application at `http://localhost:5000`

## Deployment to Digital Ocean

### Option 1: Docker on a Droplet

1. Create a Digital Ocean Droplet (Ubuntu 22.04 recommended)

2. SSH into your droplet:
```bash
ssh root@your-droplet-ip
```

3. Install Docker and Docker Compose:
```bash
apt update
apt install -y docker.io docker-compose
systemctl start docker
systemctl enable docker
```

4. Clone or upload your application files to the droplet

5. Run with Docker Compose:
```bash
docker-compose up -d
```

6. Configure firewall to allow port 5000 (or use nginx as reverse proxy)

### Option 2: Digital Ocean App Platform

1. Push your code to a Git repository (GitHub, GitLab, etc.)

2. Go to Digital Ocean App Platform

3. Create a new app and connect your repository

4. Configure build settings:
   - Build Command: (leave empty, Docker will handle it)
   - Run Command: `gunicorn --bind 0.0.0.0:5000 --workers 4 app:app`

5. Add environment variables if needed

6. Deploy!

### Option 3: Using nginx as Reverse Proxy (Recommended for Production)

1. Install nginx on your droplet:
```bash
apt install -y nginx
```

2. Create nginx configuration (`/etc/nginx/sites-available/survey-viewer`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 20M;
}
```

3. Enable the site:
```bash
ln -s /etc/nginx/sites-available/survey-viewer /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

4. Install SSL certificate with Let's Encrypt (optional but recommended):
```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

## Usage

1. **Upload a Survey**: Click "Choose a file" on the home page, select your CSV or Excel file, and click "Upload"

2. **View Data**: After upload, you'll be redirected to the survey view page

3. **Filter Data**: Use the dropdown filters to filter by specific column values

4. **Search**: Use the global search box to search across all columns

5. **Sort**: Click on column headers to sort

6. **Export**: Export filtered data as CSV or JSON

7. **Manage Surveys**: Return to the home page to view all uploaded surveys or delete old ones

## File Structure

```
nac-data-tool/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .gitignore           # Git ignore file
├── README.md            # This file
├── static/
│   ├── css/
│   │   └── style.css    # Styles
│   └── js/
│       ├── main.js      # Home page JavaScript
│       └── survey.js    # Survey view JavaScript
├── templates/
│   ├── index.html       # Home page template
│   └── survey.html      # Survey view template
├── uploads/             # Uploaded files (auto-created)
└── data/                # SQLite database and JSON files (auto-created)
```

## Configuration

You can modify these settings in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `ALLOWED_EXTENSIONS`: Allowed file types (default: csv, xlsx, xls)

## Security Notes

For production deployment:

1. Change Flask's secret key (add `app.secret_key` in app.py)
2. Use environment variables for sensitive configuration
3. Set up proper authentication if needed
4. Use HTTPS (SSL certificate)
5. Configure firewall rules
6. Regular backups of the `data/` directory
7. Consider adding rate limiting for uploads

## Troubleshooting

**Upload fails**: Check file size and format. Ensure uploads/ directory is writable.

**Data not displaying**: Check browser console for errors. Ensure data/ directory is writable.

**Docker issues**: Make sure ports are not already in use. Check Docker logs with `docker-compose logs`.

## 📚 Documentation

Comprehensive documentation is available in the project:

- **[Quick Filter Guide](docs/QUICK_FILTER_GUIDE.md)** - Complete guide to the new Quick Filter Grid (v3.0)
- **[CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md)** - Technical reference for developers
- **[CLAUDE.md](CLAUDE.md)** - Development history and architecture decisions
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[COMPARISON_GUIDE.md](COMPARISON_GUIDE.md)** - Multi-scenario comparison guide
- **[CROSSTAB_VIEWER_GUIDE.md](CROSSTAB_VIEWER_GUIDE.md)** - Crosstab/banner table guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment options and configurations
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference for common tasks

## Version History

- **v3.0** (January 2025) - Quick Filter Grid with dual modes, duplicate filters, bulk actions
- **v2.1** (December 2024) - Multi-scenario comparison, crosstab viewer enhancements
- **v2.0** (November 2024) - Cross-question analysis, SPSS support, crosstab parser
- **v1.0** (October 2024) - Initial release with CSV/Excel upload, filtering, charts

## License

MIT License - feel free to use and modify as needed.
