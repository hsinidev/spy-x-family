# 🕵️ Operation Strix: Deployment Manual

This guide outlines the steps to deploy the **Spy X Family Portal** to a public VPS (Ubuntu/Debian recommended) using Nginx.

## 1. Server Prerequisites
Before proceeding, ensure your VPS has the following installed:
*   **Nginx**: `sudo apt update && sudo apt install nginx`
*   **Certbot (for SSL)**: `sudo apt install certbot python3-certbot-nginx`

## 2. Directory Setup
Create the target directory on your server:
```bash
sudo mkdir -p /var/www/spy-x-family
sudo chown -R $USER:$USER /var/www/spy-x-family
```

## 3. Deployment Steps
You have two options to deploy:

### Option A: Using the Deployment Script (Linux/Mac)
1. Edit `deploy.sh` and replace `YOUR_VPS_IP` with your server's IP address.
2. Run the script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Option B: Manual Upload
1. Use FileZilla or WinSCP to upload all files to `/var/www/spy-x-family`.
2. Copy `nginx.conf` to Nginx's sites-available:
   ```bash
   sudo cp /var/www/spy-x-family/nginx.conf /etc/nginx/sites-available/spy-x-family
   sudo ln -s /etc/nginx/sites-available/spy-x-family /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## 4. Enabling HTTPS (Crucial for PWA)
Run Certbot to secure your domain:
```bash
sudo certbot --nginx -d readspyxfamily.org -d www.readspyxfamily.org
```

## 5. Post-Deployment Verification
*   Visit your domain.
*   Open DevTools > Application > Service Workers to ensure `sw.js` is active.
*   Test the "Mission_Archive" search to ensure all chapter routing is functional.

---
**CLASSIFIED INFORMATION:** DO NOT SHARE SERVER IP UNLESS NECESSARY.
**© 2024 WISE INTELLIGENCE HUB**
