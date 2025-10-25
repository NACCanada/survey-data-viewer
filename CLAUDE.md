# Survey Data Viewer - Development with Claude

This project was built with assistance from Claude (Anthropic's AI assistant) to create a production-ready survey data visualization tool.

---

## 🚀 FOR CLAUDE: START HERE

**⚠️ IMPORTANT: To save tokens and avoid re-analyzing files, read `CODEBASE_SUMMARY.md` first!**

That file contains:
- Complete file structure and API documentation
- Key features and implementation details
- Common modification locations with line numbers
- Data flow diagrams
- Quick reference for common tasks

Only read specific files when you need to modify them. The summary should answer most questions about the codebase structure.

---

## Project Overview

**Survey Data Viewer** is a lightweight web application for uploading, visualizing, filtering, and comparing CSV/Excel survey data. Built with Flask, DataTables, and Chart.js.

## Development Journey

### Initial Requirements
- Upload CSV/Excel files and generate unique pages
- Auto-populate filters from column headings
- Lightweight and easy to deploy
- Host on Digital Ocean or similar

### Built Features

#### Core Features (v1.0)
- ✅ File upload (CSV/Excel support)
- ✅ Automatic page generation with unique URLs
- ✅ Dynamic filters based on column values
- ✅ Sortable, searchable data tables
- ✅ Export to CSV/JSON
- ✅ SQLite database for metadata
- ✅ Responsive design

#### Enhanced Features (v2.0)
- ✅ Interactive charts with Chart.js
- ✅ Automatic chart generation for categorical data
- ✅ Toggle chart visibility
- ✅ Environment-based configuration
- ✅ Production deployment setup

#### Comparison Mode (v2.1)
- ✅ Side-by-side data comparison
- ✅ Group A vs Group B filtering
- ✅ Comparison charts with grouped bars
- ✅ Real-time updates
- ✅ Individual group clear buttons

#### Bug Fixes & Improvements
- ✅ Fixed numeric filter comparisons (string vs number)
- ✅ Enhanced filter logic for mixed data types
- ✅ Added clear buttons for comparison groups
- ✅ Improved UI/UX throughout

## Technology Stack

**Backend:**
- Flask 3.0.0
- pandas 2.1.4
- openpyxl 3.1.2
- python-dotenv 1.0.0
- gunicorn 21.2.0

**Frontend:**
- Vanilla JavaScript (no framework)
- jQuery 3.7.1
- DataTables 1.13.7
- Chart.js 4.4.0
- Custom CSS with gradients

**Database:**
- SQLite (for metadata)
- JSON files (for survey data)

**Deployment:**
- Docker & Docker Compose
- nginx reverse proxy
- Systemd service configuration
- Digital Ocean ready

## Architecture Decisions

### Why These Technologies?

1. **Flask**: Lightweight, easy to deploy, perfect for small-to-medium apps
2. **SQLite**: No separate DB server needed, embedded, perfect for metadata
3. **JSON Storage**: Fast reads, easy to work with, good for <10k rows per survey
4. **DataTables**: Mature, feature-rich, handles sorting/filtering client-side
5. **Chart.js**: Popular, well-documented, responsive charts
6. **Vanilla JS**: No build step, fast loading, easy maintenance

### Design Patterns

- **MVC-ish**: Templates (View), Flask routes (Controller), Data layer (Model)
- **Progressive Enhancement**: Works without JS for basic viewing
- **Client-side Processing**: Filters and charts render in browser for speed
- **RESTful API**: `/api/survey/<id>/data` endpoint for data access

### File Structure
```
nac-data-tool/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-container setup
├── deploy.sh                  # Automated deployment script
├── nginx.conf                 # Reverse proxy config
├── static/
│   ├── css/style.css         # All styling
│   └── js/
│       ├── main.js           # Home page functionality
│       └── survey.js         # Survey view (filters, charts, comparison)
├── templates/
│   ├── index.html            # Home/upload page
│   └── survey.html           # Survey view page
├── uploads/                   # Uploaded files
├── data/                      # SQLite DB + JSON data files
└── docs/
    ├── README.md             # Main documentation
    ├── QUICKSTART.md         # 5-minute setup guide
    ├── FEATURES.md           # Complete feature list
    ├── DEPLOYMENT.md         # Deployment guide
    └── COMPARISON_GUIDE.md   # Comparison mode guide
```

## Key Implementation Details

### Filter System
- Detects columns with ≤100 unique values
- Auto-generates dropdown filters
- Handles both string and numeric comparisons
- Real-time filtering without page reload

### Chart Generation
- Detects columns with ≤20 unique values
- Creates bar charts automatically
- Color-coded categories
- Responsive and printable

### Comparison Mode
- Independent filter sets for Group A and B
- Side-by-side visualization
- Grouped bar charts for comparisons
- Real-time count updates

### Performance
- Tested with 1000+ row datasets
- Client-side filtering (instant)
- Pagination for large tables
- Lazy loading for charts

## Development Process

### Iterative Enhancement
1. Started with basic upload/view functionality
2. Added filtering and search
3. Introduced charts for visualization
4. Implemented comparison mode
5. Enhanced deployment options
6. Fixed bugs and improved UX

### Testing Approach
- Created sample datasets (10 rows, 1000 rows)
- Tested with various data types (numeric, text, dates)
- Verified on different screen sizes
- Tested deployment configurations

## Deployment Options

### 1. Local Development
```bash
pip install -r requirements.txt
python app.py
# Access at http://localhost:8080
```

### 2. Docker Compose (Recommended)
```bash
docker-compose up -d
# Access at http://localhost
```

### 3. Digital Ocean Droplet
```bash
# Upload files
scp -r . root@droplet:/opt/survey-viewer

# Run deployment script
ssh root@droplet
cd /opt/survey-viewer
bash deploy.sh
```

### 4. App Platform (PaaS)
- Push to GitHub
- Connect repository in DO App Platform
- Auto-deploy on push

## Security Considerations

### Implemented
- ✅ Secure filename handling (werkzeug)
- ✅ File type validation
- ✅ File size limits (16MB)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Environment-based secrets

### Recommended for Production
- [ ] Add authentication/authorization
- [ ] Rate limiting on uploads
- [ ] HTTPS/SSL certificates
- [ ] Regular backups
- [ ] Input sanitization for user feedback
- [ ] CSRF protection

## Known Limitations

1. **Scale**: Best for <10k rows per survey (client-side rendering)
2. **Storage**: Files stored on disk (not S3/cloud storage)
3. **Auth**: No built-in user authentication
4. **Collaboration**: No multi-user editing or permissions
5. **Statistics**: No advanced stats (mean, median, p-values)

## Future Enhancement Ideas

### Short Term
- [ ] Pie charts for binary data
- [ ] Line charts for time-series
- [ ] Export charts as images
- [ ] Dark mode toggle

### Medium Term
- [ ] User authentication (OAuth)
- [ ] Team/organization support
- [ ] Survey templates
- [ ] Scheduled data exports
- [ ] Email notifications

### Long Term
- [ ] Real-time collaboration
- [ ] Advanced statistics & analysis
- [ ] Machine learning insights
- [ ] API for integrations
- [ ] Mobile app

## Lessons Learned

### What Worked Well
- ✅ Starting simple and iterating
- ✅ Client-side rendering for responsiveness
- ✅ Comprehensive documentation
- ✅ Multiple deployment options
- ✅ Real data testing (1000 row dataset)

### What Could Be Improved
- More automated testing (unit/integration tests)
- Earlier consideration of authentication
- More modular JavaScript (consider splitting survey.js)
- Performance profiling with larger datasets

## Contributing

This project was built as a demonstration of rapid application development with AI assistance. For production use, consider:

1. Adding comprehensive test coverage
2. Implementing proper authentication
3. Setting up CI/CD pipelines
4. Adding monitoring and logging
5. Implementing proper error handling

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [DataTables Documentation](https://datatables.net/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Digital Ocean Deployment Guides](https://www.digitalocean.com/community/tutorials)

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with Claude (Anthropic) - An AI assistant that helped with:
- Architecture and design decisions
- Code implementation
- Documentation writing
- Deployment configuration
- Bug fixing and optimization

---

**Built**: October 2025
**Version**: 2.1
**Status**: Production Ready
**Deployed**: Ready for Digital Ocean, Docker, or local hosting
