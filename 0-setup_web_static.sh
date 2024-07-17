#!/bin/bash
# 0-setup_web_static.sh
# This script sets up web servers for the deployment of web_static.

# Install Nginx if not already installed
apt-get update
apt-get install -y nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file for testing
echo	 "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create symbolic link
rm -f /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

# Set ownership recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
CONFIG_FILE="/etc/nginx/sites-available/default"
echo "server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        autoindex off;
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}" > "$CONFIG_FILE"

# Restart Nginx
service nginx restart
