#!/bin/bash

# Deployment script for Digital Ocean droplet

set -e

echo "======================================"
echo "Survey Data Viewer - Deployment Script"
echo "======================================"

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install required packages
echo "Installing dependencies..."
apt-get install -y python3 python3-pip python3-venv nginx git

# Create application directory
APP_DIR="/opt/survey-viewer"
echo "Setting up application in $APP_DIR..."
mkdir -p $APP_DIR

# Copy files (assumes you're running from project directory)
echo "Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads data

# Set up environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i "s/your-secret-key-here-change-this/$SECRET_KEY/" .env
fi

# Set proper permissions
echo "Setting permissions..."
chown -R www-data:www-data $APP_DIR
chmod 755 $APP_DIR
chmod -R 755 uploads data

# Create systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/survey-viewer.service <<EOF
[Unit]
Description=Survey Data Viewer
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 120 app:app

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
echo "Configuring nginx..."
cp nginx.conf /etc/nginx/sites-available/survey-viewer
ln -sf /etc/nginx/sites-available/survey-viewer /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

# Enable and start services
echo "Starting services..."
systemctl daemon-reload
systemctl enable survey-viewer
systemctl start survey-viewer
systemctl restart nginx

# Check status
echo ""
echo "======================================"
echo "Deployment complete!"
echo "======================================"
echo "Service status:"
systemctl status survey-viewer --no-pager
echo ""
echo "Nginx status:"
systemctl status nginx --no-pager
echo ""
echo "Access your application at: http://$(curl -s ifconfig.me)"
echo ""
