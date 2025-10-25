# Ubuntu Deployment Guide

## System Requirements

- **Ubuntu**: 20.04 LTS or newer (22.04 LTS recommended)
- **Python**: 3.8 or newer (3.10+ recommended)
- **RAM**: 2GB minimum, 4GB+ recommended for large datasets
- **Storage**: 10GB minimum for application and data

## Prerequisites Installation

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and build tools
sudo apt-get install -y python3 python3-pip python3-dev python3-venv
sudo apt-get install -y build-essential git

# For SAV file support (SPSS files)
sudo apt-get install -y build-essential python3-dev

# Optional: Install nginx for production deployment
sudo apt-get install -y nginx
```

## Application Setup

### 1. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/NACCanada/survey-data-viewer.git
sudo chown -R $USER:$USER survey-data-viewer
cd survey-data-viewer
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If `pyreadstat` fails to install, ensure build tools are installed:
```bash
sudo apt-get install build-essential python3-dev
pip install pyreadstat
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env
```

Set the following:
```
FLASK_SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=your-admin-password
UPLOAD_FOLDER=uploads
DATA_FOLDER=data
```

### 5. Create Required Directories

```bash
mkdir -p uploads data
chmod 755 uploads data
```

## Running the Application

### Development Mode

```bash
source venv/bin/activate
python app.py
```

Access at: `http://localhost:8080`

### Production Mode with Gunicorn

```bash
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

Options:
- `-w 4`: 4 worker processes (adjust based on CPU cores)
- `-b 0.0.0.0:8080`: Bind to all interfaces on port 8080
- `--timeout 120`: Increase timeout for large file uploads

### Systemd Service (Recommended for Production)

Create service file:
```bash
sudo nano /etc/systemd/system/survey-viewer.service
```

Contents:
```ini
[Unit]
Description=Survey Data Viewer
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/survey-data-viewer
Environment="PATH=/opt/survey-data-viewer/venv/bin"
ExecStart=/opt/survey-data-viewer/venv/bin/gunicorn -w 4 -b 127.0.0.1:8080 --timeout 120 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable survey-viewer
sudo systemctl start survey-viewer
sudo systemctl status survey-viewer
```

## Nginx Reverse Proxy (Optional)

Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/survey-viewer
```

Contents:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for large file processing
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/survey-viewer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Or allow specific port if not using nginx
sudo ufw allow 8080/tcp

sudo ufw enable
```

## Verification

1. **Check Dependencies**:
   ```bash
   python3 -c "import flask, pandas, openpyxl, pyreadstat; print('All dependencies OK')"
   ```

2. **Test File Operations**:
   ```bash
   python3 << 'EOF'
   import os
   test_file = os.path.join('data', 'test.json')
   with open(test_file, 'w') as f:
       f.write('{"test": "data"}')
   os.remove(test_file)
   print("File operations OK")
   EOF
   ```

3. **Access Application**:
   - Development: http://localhost:8080
   - Production: http://your-server-ip or http://your-domain.com

## Troubleshooting

### Permission Issues
```bash
sudo chown -R $USER:$USER /opt/survey-data-viewer
chmod 755 uploads data
```

### Port Already in Use
```bash
# Find process using port 8080
sudo lsof -i :8080
# Kill if needed
sudo kill -9 <PID>
```

### Pyreadstat Installation Fails
```bash
sudo apt-get install build-essential python3-dev zlib1g-dev
pip install --no-cache-dir pyreadstat
```

### Service Won't Start
```bash
sudo journalctl -u survey-viewer -n 50
```

## Security Recommendations

1. **Change default passwords** in `.env`
2. **Use HTTPS** with Let's Encrypt:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```
3. **Set up firewall** with ufw
4. **Regular backups** of `data/` folder
5. **Keep dependencies updated**:
   ```bash
   pip list --outdated
   ```

## Updating the Application

```bash
cd /opt/survey-data-viewer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart survey-viewer
```

## Performance Tuning

### For Large Datasets
Edit gunicorn configuration:
```bash
gunicorn -w 4 --threads 2 --worker-class gthread \
  --timeout 300 --max-requests 1000 --max-requests-jitter 50 \
  -b 0.0.0.0:8080 app:app
```

### Memory Optimization
```bash
# Limit gunicorn workers based on RAM
# Formula: (2 x CPU cores) + 1, but adjust for available RAM
# Each worker uses ~200-500MB
```

## Compatibility Notes

✅ **Fully Compatible**:
- All Python dependencies are cross-platform
- File paths use `os.path.join()` (cross-platform)
- UTF-8 encoding handled correctly
- No OS-specific system calls

✅ **Tested On**:
- macOS (development)
- Ubuntu 20.04 LTS
- Ubuntu 22.04 LTS

⚠️ **Known Requirements**:
- Build tools needed for `pyreadstat` (SPSS file support)
- Python 3.8+ required
- 2GB+ RAM for processing large files

## Support

For issues or questions:
- GitHub Issues: https://github.com/NACCanada/survey-data-viewer/issues
- Check logs: `sudo journalctl -u survey-viewer -f`
