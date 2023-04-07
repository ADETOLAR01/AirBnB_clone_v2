#!/usr/bin/env bash

# Install Nginx if it is not installed
if [ ! -x "$(command -v nginx)" ]; then
  sudo apt-get update
  sudo apt-get -y install nginx
fi

# Create necessary folders
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared /data/web_static/current

# Create fake HTML file
echo "<html><head><title>Test</title></head><body><p>This is a test.</p></body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '38i\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
