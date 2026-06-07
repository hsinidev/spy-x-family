#!/bin/bash

# --- DEPLOYMENT CONFIGURATION ---
VPS_USER="root"
VPS_IP="YOUR_VPS_IP"
REMOTE_DIR="/var/www/spy-x-family"
# --------------------------------

echo "[INTEL]: Commencing Operation Upload..."

# Check if rsync is installed
if ! command -v rsync &> /dev/null
then
    echo "[ERROR]: rsync is not installed. Please install it to proceed."
    exit 1
fi

# Upload files using rsync (excluding local dev noise)
rsync -avz --progress \
    --exclude '.git/' \
    --exclude '.gemini/' \
    --exclude 'node_modules/' \
    --exclude 'scratch/' \
    --exclude 'standardize_site.py' \
    --exclude 'deploy.sh' \
    ./ ${VPS_USER}@${VPS_IP}:${REMOTE_DIR}

echo "[SUCCESS]: Files successfully infiltrated ${VPS_IP}."

echo "[INTEL]: Updating Nginx Configuration..."
ssh ${VPS_USER}@${VPS_IP} "ln -sf ${REMOTE_DIR}/nginx.conf /etc/nginx/sites-enabled/spy-x-family && nginx -t && systemctl reload nginx"

echo "[COMPLETE]: Operation Strix is now live."
