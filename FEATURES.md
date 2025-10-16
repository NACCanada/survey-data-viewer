# Survey Data Viewer - Features Guide

## Overview
A lightweight web application for visualizing, filtering, and analyzing CSV and Excel survey data.

---

## Core Features

### 1. File Upload & Processing
- **Supported Formats**: CSV, Excel (.xlsx, .xls)
- **Max File Size**: 16MB (configurable)
- **Automatic Processing**: Data automatically parsed and validated
- **Unique URLs**: Each upload gets a unique ID and permanent URL

### 2. Data Visualization (NEW!)

#### Interactive Charts
- **Automatic Chart Generation**: Creates bar charts for categorical data
- **Smart Detection**: Only creates charts for columns with ≤20 unique values
- **Color-Coded**: Beautiful, distinct colors for each category
- **Toggle Visibility**: Show/hide all charts with one click
- **Responsive**: Charts adapt to screen size

#### Chart Types
- Bar charts for categorical data (Department, Satisfaction, etc.)
- Counts and distributions automatically calculated
- Clean, professional design matching app theme

### 3. Dynamic Filtering

#### Column-Based Filters
- **Auto-Generated**: Filters created automatically from column data
- **Dropdown Menus**: Easy selection for categorical values
- **Smart Limits**: Only columns with ≤100 unique values get filters
- **Real-Time**: Instant filtering without page reload
- **Clear All**: Reset all filters with one click

#### Global Search
- Search across all columns simultaneously
- Highlight matching results
- Case-insensitive search
- Works with filters

### 4. Data Table Features

#### Sorting
- Click any column header to sort
- Ascending/descending toggle
- Multi-column sorting support

#### Pagination
- Choose entries per page (10, 25, 50, 100, or All)
- Navigate between pages easily
- Shows current page and total entries

#### Responsive Design
- Horizontal scrolling for many columns
- Mobile-friendly interface
- Adapts to screen size

### 5. Data Export

#### CSV Export
- Export filtered/searched data only
- Maintains proper CSV formatting
- Handles special characters and quotes
- Downloads directly to your computer

#### JSON Export
- Clean JSON format with proper indentation
- Export filtered results
- Great for API integration or further processing

### 6. Survey Management

#### Dashboard
- View all uploaded surveys in one place
- See row counts and upload dates
- Quick access to any survey
- Search and organize

#### Delete Function
- Remove surveys you no longer need
- Cleans up database and files
- Confirmation prompt for safety

---

## Technical Improvements

### Deployment Enhancements

#### Environment Variables
- Configurable via `.env` file
- Secret key management
- Port and host configuration
- Max file size control

#### Docker Support
- Multi-container setup with nginx
- Persistent volumes for data
- Production-ready configuration
- Easy scaling

#### nginx Integration
- Reverse proxy setup
- Static file caching
- SSL/HTTPS support
- Request timeout configuration

#### Systemd Service
- Auto-start on boot
- Process monitoring
- Automatic restart on failure
- Easy log access

### Security Features
- Secret key for session management
- Secure file upload handling
- SQL injection prevention
- XSS protection
- File type validation

### Performance
- Client-side filtering for speed
- Efficient data loading
- Minimal server overhead
- CDN for libraries (jQuery, DataTables, Chart.js)

---

## User Workflows

### Basic Workflow
1. Upload CSV/Excel file
2. View auto-generated charts
3. Apply filters to narrow data
4. Search for specific entries
5. Export filtered results

### Analysis Workflow
1. Upload survey results
2. Review visualizations to spot trends
3. Use filters to segment data
4. Compare different segments
5. Export findings for reports

### Multi-Survey Workflow
1. Upload multiple survey files
2. Each gets unique URL for sharing
3. Compare across surveys
4. Maintain data separately
5. Delete old surveys when done

---

## Chart Capabilities

### What Gets Charted?
- Columns with categorical data (text values)
- Columns with ≤20 unique values
- Automatic count aggregation
- Clear labels and legends

### Chart Interactions
- Hover to see exact counts
- Toggle visibility to focus on tables
- Responsive to screen size
- Print-friendly

### Examples of Good Chart Data
- ✅ Department (Engineering, Sales, Marketing)
- ✅ Satisfaction Level (Very Satisfied, Satisfied, Neutral, etc.)
- ✅ Yes/No questions
- ✅ Rating scales (1-5 stars)
- ✅ Categories with ~5-20 options

### What Doesn't Get Charted?
- ❌ Unique identifiers (IDs, emails)
- ❌ Free text responses
- ❌ Columns with >20 unique values
- ❌ Continuous numeric data (use filters instead)

---

## Browser Compatibility
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

---

## Performance Specs

### Tested Capacity
- **Small surveys**: <100 rows - Instant loading
- **Medium surveys**: 100-1,000 rows - <2 seconds
- **Large surveys**: 1,000-10,000 rows - <5 seconds
- **Very large**: 10,000+ rows - May require pagination

### Concurrent Users
- **Basic droplet ($6/mo)**: ~10-20 simultaneous users
- **Standard droplet ($12/mo)**: ~50-100 simultaneous users

---

## Tips & Best Practices

### For Best Charts
1. Keep categorical columns to <20 unique values
2. Use consistent naming (not "Yes", "yes", "YES")
3. Avoid empty cells where possible
4. Use clear, descriptive column names

### For Best Performance
1. Clean data before uploading
2. Remove unnecessary columns
3. Use filters instead of re-uploading
4. Export only what you need

### For Collaboration
1. Share survey URLs with team members
2. Export filtered results for reports
3. Keep surveys organized with clear filenames
4. Delete old surveys regularly

---

## Keyboard Shortcuts
- `Tab`: Navigate between filters
- `Enter`: Apply search
- `Esc`: Clear current filter/search (browser default)

---

## Future Enhancement Ideas
- Pie charts for yes/no questions
- Line charts for time-series data
- Export charts as images
- Email notifications for uploads
- User authentication
- Survey comparison view
- Custom color themes
- Advanced statistics (mean, median, etc.)

---

## Getting Help
- Check README.md for setup instructions
- See DEPLOYMENT.md for deployment guides
- Check browser console for errors
- Review application logs for issues

---

## Changelog

### Version 2.0 (Current)
- ✨ Added interactive charts with Chart.js
- ✨ Added chart toggle functionality
- 🔧 Environment variable configuration
- 🔧 nginx reverse proxy support
- 🔧 Docker Compose with multi-container setup
- 🔧 Automated deployment script
- 📚 Comprehensive deployment documentation

### Version 1.0
- 📤 File upload (CSV/Excel)
- 🔍 Dynamic filters
- 🔎 Global search
- 📊 Data table with sorting/pagination
- 📥 Export to CSV/JSON
- 🗑️ Survey management
