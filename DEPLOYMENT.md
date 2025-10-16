# Deployment Guide

This guide covers multiple deployment options for the Survey Data Viewer application.

## Quick Deployment Summary

| Method | Difficulty | Cost | Best For |
|--------|-----------|------|----------|
| Docker Compose | Easy | $6-12/mo | Quick deployment, full control |
| Digital Ocean App Platform | Easiest | $5+/mo | Hands-off managed solution |
| Manual Setup + nginx | Medium | $6-12/mo | Production-grade, custom configuration |

---

## Option 1: Docker Compose (Recommended for Beginners)

### Prerequisites
- Digital Ocean Droplet (Ubuntu 22.04, $6/month Basic Droplet)
- Domain name (optional, can use IP address)

### Steps

1. **Create a Droplet**
   ```bash
   # On Digital Ocean dashboard:
   # - Create Droplet
   # - Choose Ubuntu 22.04
   # - Basic plan ($6/month)
   # - Add your SSH key
   ```

2. **SSH into your droplet**
   ```bash
   ssh root@YOUR_DROPLET_IP
   ```

3. **Install Docker & Docker Compose**
   ```bash
   apt update
   apt install -y docker.io docker-compose git
   systemctl start docker
   systemctl enable docker
   ```

4. **Clone/Upload your code**
   ```bash
   # Option A: Using git
   git clone YOUR_REPO_URL /opt/survey-viewer

   # Option B: Using SCP from your local machine
   scp -r /path/to/nac-data-tool root@YOUR_DROPLET_IP:/opt/survey-viewer
   ```

5. **Configure environment**
   ```bash
   cd /opt/survey-viewer
   cp .env.example .env
   nano .env  # Edit SECRET_KEY and other settings
   ```

6. **Start the application**
   ```bash
   docker-compose up -d
   ```

7. **Access your app**
   - Visit: `http://YOUR_DROPLET_IP`

### Updating
```bash
cd /opt/survey-viewer
git pull  # or upload new files
docker-compose down
docker-compose up -d --build
```

---

## Option 2: Digital Ocean App Platform (Easiest)

### Prerequisites
- GitHub/GitLab repository with your code
- Digital Ocean account

### Steps

1. **Push code to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

2. **Create App on Digital Ocean**
   - Go to App Platform in Digital Ocean dashboard
   - Click "Create App"
   - Connect your GitHub/GitLab repository
   - Select your repository and branch

3. **Configure Build Settings**
   - **Build Command**: (leave empty)
   - **Run Command**: `gunicorn --bind 0.0.0.0:8080 --workers 4 app:app`
   - **Environment Variables**:
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-random-secret-key`
     - `PORT=8080`

4. **Configure Resources**
   - Select Basic plan ($5/month)
   - Add persistent storage for `/app/uploads` and `/app/data`

5. **Deploy**
   - Click "Next" and then "Create Resources"
   - Wait for deployment (5-10 minutes)
   - Access your app at the provided URL

### Updating
- Simply push to your Git repository
- App Platform auto-deploys on push

---

## Option 3: Manual Setup with nginx (Production-Grade)

### Prerequisites
- Digital Ocean Droplet (Ubuntu 22.04)
- Domain name pointed to your droplet IP

### Automated Deployment

1. **Upload and run deployment script**
   ```bash
   scp deploy.sh root@YOUR_DROPLET_IP:/tmp/
   ssh root@YOUR_DROPLET_IP
   cd /tmp
   bash deploy.sh
   ```

### Manual Deployment Steps

1. **SSH into droplet**
   ```bash
   ssh root@YOUR_DROPLET_IP
   ```

2. **Install dependencies**
   ```bash
   apt update
   apt install -y python3 python3-pip python3-venv nginx git
   ```

3. **Set up application**
   ```bash
   mkdir -p /opt/survey-viewer
   cd /opt/survey-viewer

   # Upload your files or git clone

   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   mkdir -p uploads data
   cp .env.example .env
   nano .env  # Configure environment variables
   ```

4. **Create systemd service**
   ```bash
   nano /etc/systemd/system/survey-viewer.service
   ```

   Paste:
   ```ini
   [Unit]
   Description=Survey Data Viewer
   After=network.target

   [Service]
   Type=notify
   User=www-data
   Group=www-data
   WorkingDirectory=/opt/survey-viewer
   Environment="PATH=/opt/survey-viewer/venv/bin"
   ExecStart=/opt/survey-viewer/venv/bin/gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 120 app:app

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure nginx**
   ```bash
   cp nginx.conf /etc/nginx/sites-available/survey-viewer
   ln -s /etc/nginx/sites-available/survey-viewer /etc/nginx/sites-enabled/
   rm /etc/nginx/sites-enabled/default

   # Edit nginx config with your domain
   nano /etc/nginx/sites-available/survey-viewer
   ```

6. **Set permissions**
   ```bash
   chown -R www-data:www-data /opt/survey-viewer
   chmod -R 755 /opt/survey-viewer/uploads /opt/survey-viewer/data
   ```

7. **Start services**
   ```bash
   systemctl daemon-reload
   systemctl enable survey-viewer
   systemctl start survey-viewer
   systemctl restart nginx
   ```

8. **Set up SSL (Optional but Recommended)**
   ```bash
   apt install -y certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com
   ```

### Updating
```bash
cd /opt/survey-viewer
source venv/bin/activate
git pull  # or upload new files
pip install -r requirements.txt
systemctl restart survey-viewer
```

---

## Monitoring & Maintenance

### Check Application Status
```bash
systemctl status survey-viewer
```

### View Logs
```bash
# Application logs
journalctl -u survey-viewer -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Docker logs
docker-compose logs -f
```

### Backup Data
```bash
# Backup database and uploads
tar -czf backup-$(date +%Y%m%d).tar.gz data/ uploads/

# Download backup
scp root@YOUR_DROPLET_IP:/opt/survey-viewer/backup-*.tar.gz ./
```

### Restore Data
```bash
tar -xzf backup-YYYYMMDD.tar.gz
systemctl restart survey-viewer
```

---

## Security Considerations

### Essential Security Steps

1. **Change default SECRET_KEY**
   ```bash
   # Generate a secure key
   python3 -c "import secrets; print(secrets.token_hex(32))"
   # Add to .env file
   ```

2. **Set up firewall**
   ```bash
   ufw allow 22/tcp   # SSH
   ufw allow 80/tcp   # HTTP
   ufw allow 443/tcp  # HTTPS
   ufw enable
   ```

3. **Enable automatic security updates**
   ```bash
   apt install unattended-upgrades
   dpkg-reconfigure -plow unattended-upgrades
   ```

4. **Regular backups**
   - Set up automated daily backups of `/opt/survey-viewer/data`
   - Use Digital Ocean Snapshots (weekly recommended)

5. **Monitor disk usage**
   ```bash
   df -h  # Check disk space
   du -sh uploads/ data/  # Check app storage
   ```

---

## Troubleshooting

### Application won't start
```bash
# Check service status
systemctl status survey-viewer

# Check logs for errors
journalctl -u survey-viewer -n 50

# Test app manually
cd /opt/survey-viewer
source venv/bin/activate
python app.py
```

### Can't upload files
```bash
# Check permissions
ls -la /opt/survey-viewer/uploads
chown -R www-data:www-data /opt/survey-viewer/uploads
chmod 755 /opt/survey-viewer/uploads
```

### nginx errors
```bash
# Test nginx configuration
nginx -t

# Reload nginx
systemctl reload nginx

# Check nginx logs
tail -f /var/log/nginx/error.log
```

### Out of disk space
```bash
# Check disk usage
df -h

# Clean up old uploads (be careful!)
find /opt/survey-viewer/uploads -type f -mtime +90 -delete

# Clean up Docker (if using Docker)
docker system prune -a
```

---

## Performance Optimization

### For High Traffic

1. **Increase Gunicorn workers**
   ```bash
   # Edit systemd service
   ExecStart=... --workers 8 ...
   ```

2. **Add nginx caching**
   ```nginx
   location /static {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

3. **Upgrade droplet**
   - More RAM for larger datasets
   - More CPU for concurrent uploads

4. **Use PostgreSQL instead of SQLite**
   - Better for concurrent access
   - Required for >100 concurrent users

---

## Cost Breakdown

### Digital Ocean Droplet
- Basic ($6/mo): 1GB RAM, 25GB SSD - Good for <100 surveys
- Standard ($12/mo): 2GB RAM, 50GB SSD - Good for <500 surveys
- Enhanced ($18/mo): 2GB RAM, 60GB SSD - Good for <1000 surveys

### Digital Ocean App Platform
- Basic ($5/mo): 512MB RAM - Good for light usage
- Professional ($12/mo): 1GB RAM - Good for moderate usage

### Additional Costs
- Domain name: $10-15/year
- Backups (Droplet Snapshots): $1-2/month
- Block Storage (optional): $1/10GB/month

---

## Next Steps

1. Choose your deployment method
2. Follow the steps above
3. Test thoroughly with sample data
4. Set up backups
5. Configure SSL certificate
6. Monitor for first few days

For questions or issues, check the README.md or create an issue on GitHub.
