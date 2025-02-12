#!/bin/bash

# Define paths
CLIENT_DIR="webapp/dashboard_client"
SERVER_DIR="webapp/dashboard_server"
NGINX_DIR="/var/www/html"

# Navigate to client folder
cd /home/pi
cd "$CLIENT_DIR"
sudo -u pi git pull
npm install
npm run build
rm -rf /var/www/html/*
mv dist/* "$NGINX_DIR"

cd /home/pi
cd "$SERVER_DIR"
source venv/bin/activate
sudo -u pi git pull
pip install -r requirements.txt

systemctl restart flaskapp
systemctl restart nginx
#DISPLAY=:0 xdotool search --onlyvisible --class chromium windowactivate --sync key F5
echo "Client updated successfully!"

