# Quick Start Guide

Get your Survey Data Viewer running in under 5 minutes!

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Access
Open http://localhost:8080

That's it! 🎉

---

## Deploy to Digital Ocean (Fastest Method)

### Option 1: One-Command Deploy
```bash
# On your local machine
scp -r . root@YOUR_DROPLET_IP:/opt/survey-viewer

# On your droplet
ssh root@YOUR_DROPLET_IP
cd /opt/survey-viewer
bash deploy.sh
```
**Time**: ~5 minutes
**Cost**: $6/month

### Option 2: Docker (Easiest)
```bash
# On your droplet
git clone YOUR_REPO /opt/survey-viewer
cd /opt/survey-viewer
docker-compose up -d
```
**Time**: ~3 minutes
**Cost**: $6/month

### Option 3: App Platform (Zero Config)
1. Push code to GitHub
2. Create app on Digital Ocean
3. Connect repository
4. Deploy

**Time**: ~10 minutes (mostly waiting)
**Cost**: $5/month

---

## First Upload

1. Go to home page
2. Click "Choose a file"
3. Select your CSV or Excel file
4. Click "Upload"
5. View your data with charts and filters!

---

## What You Get

✅ **Automatic charts** for categorical data
✅ **Dynamic filters** for every column
✅ **Global search** across all data
✅ **Export** to CSV or JSON
✅ **Permanent URLs** for each survey
✅ **Mobile responsive** design

---

## Common Commands

### Start Server
```bash
python app.py
```

### Start with Docker
```bash
docker-compose up -d
```

### View Logs
```bash
# Direct
tail -f /var/log/survey-viewer.log

# Systemd
journalctl -u survey-viewer -f

# Docker
docker-compose logs -f
```

### Restart Service
```bash
systemctl restart survey-viewer
```

### Backup Data
```bash
tar -czf backup.tar.gz data/ uploads/
```

---

## Troubleshooting

### Port 5000/8080 already in use?
Change port in `app.py` or `.env` file:
```bash
PORT=9000
```

### Can't upload files?
Check permissions:
```bash
chmod 755 uploads/ data/
```

### Charts not showing?
Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)

---

## Next Steps

📖 Read [FEATURES.md](FEATURES.md) for full feature list
🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
📝 Read [README.md](README.md) for detailed documentation

---

## Support

- **Issues**: Create issue on GitHub
- **Questions**: Check documentation files
- **Updates**: `git pull` to get latest version

---

## Pro Tips

💡 Use descriptive filenames for your surveys
💡 Clean your data before uploading for best charts
💡 Share survey URLs with your team
💡 Export filtered results for reports
💡 Set up automated backups on production

---

**Ready to analyze some data?** Upload your first survey now! 📊
