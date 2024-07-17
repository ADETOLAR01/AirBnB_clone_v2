#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Exit immediately if a command exits with a non-zero status
set -e

# Install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Ensure the /data/ directory exists
if [ ! -d /data/ ]; then
    sudo mkdir -p /data/
fi

# Ensure the /data/web_static/ directory exists
if [ ! -d /data/web_static/ ]; then
    sudo mkdir -p /data/web_static/
fi

# Ensure the /data/web_static/releases/ directory exists
if [ ! -d /data/web_static/releases/ ]; then
    sudo mkdir -p /data/web_static/releases/
fi

# Ensure the /data/web_static/shared/ directory exists
if [ ! -d /data/web_static/shared/ ]; then
    sudo mkdir -p /data/web_static/shared/
fi

# Ensure the /data/web_static/releases/test/ directory exists
if [ ! -d /data/web_static/releases/test/ ]; then
    sudo mkdir -p /data/web_static/releases/test/
fi

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Welcome to web_static!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create (or recreate) the symbolic link
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current/ to hbnb_static
nginx_conf="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" $nginx_conf; then
    sudo sed -i '/server_name _;/a \\n    location /hbnb_static {\n        alias /data/web_static/current/;\n    }\n' $nginx_conf
fi

# Test Nginx configuration and restart Nginx
sudo nginx -t
sudo systemctl restart nginx

# Exit successfully
exit 0
