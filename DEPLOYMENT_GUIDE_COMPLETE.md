# 🚀 FTC Django Project - Complete Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Local Production Setup](#local-production-setup)
4. [Cloud Deployment (PythonAnywhere)](#cloud-deployment-pythonanywhere)
5. [Cloud Deployment (Heroku)](#cloud-deployment-heroku)
6. [Cloud Deployment (AWS EC2)](#cloud-deployment-aws-ec2)
7. [Cloud Deployment (DigitalOcean)](#cloud-deployment-digitalocean)
8. [Database Migration](#database-migration)
9. [Post-Deployment Checklist](#post-deployment-checklist)

---

## Prerequisites

### Required Software
- Python 3.12.10
- MySQL 5.7+ or 8.0+
- Git (for version control)
- Virtual environment tool (venv or virtualenv)

### Project Dependencies
```bash
Django==5.2.7
Pillow==10.4.0
mysqlclient  # You'll need to add this for MySQL connection
```

---

## Deployment Options

### 1️⃣ **Free Hosting Options**
- **PythonAnywhere** (Recommended for beginners) - Free tier with MySQL
- **Render** - Free tier with PostgreSQL
- **Railway** - Free tier with usage limits
- **Fly.io** - Free tier available

### 2️⃣ **Paid Hosting Options**
- **Heroku** - $5-7/month (Hobby tier)
- **DigitalOcean** - $6/month (Basic Droplet)
- **AWS EC2** - Variable pricing (Free tier for 1 year)
- **Google Cloud Platform** - Variable pricing (Free tier available)

---

## Local Production Setup

### Step 1: Prepare Your Project

1. **Update requirements.txt**
```bash
cd "c:\Users\HP.CHARANNEERUKOND\OneDrive\Desktop\FTC"
pip freeze > requirements.txt
```

2. **Create `.env` file** (for environment variables)
```bash
# Create .env file in project root
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_NAME=ftc_production
DATABASE_USER=root
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

3. **Update settings.py for production**
```python
# Add to settings.py
import os
from pathlib import Path

# Load environment variables
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME', 'ftc'),
        'USER': os.environ.get('DATABASE_USER', 'root'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '3306'),
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

4. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

---

## Cloud Deployment (PythonAnywhere)

### 🌟 **Recommended for Beginners - FREE Tier Available**

### Step 1: Create Account
1. Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Verify your email

### Step 2: Upload Your Project

**Option A: Using Git (Recommended)**
```bash
# On PythonAnywhere Bash console
cd ~
git clone https://github.com/yourusername/FTC.git
cd FTC
```

**Option B: Manual Upload**
1. Go to "Files" tab
2. Click "Upload a file"
3. Upload your project ZIP file
4. Unzip in Bash console

### Step 3: Setup Virtual Environment
```bash
# In PythonAnywhere Bash console
cd ~/FTC
mkvirtualenv --python=/usr/bin/python3.10 ftc-env
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database
1. Go to "Databases" tab
2. Create a new MySQL database (e.g., `yourusername$ftc`)
3. Note the database name, username, and password
4. Initialize database:
```bash
workon ftc-env
cd ~/FTC
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Select "Manual configuration"
4. Choose Python 3.10
5. Configure WSGI file:

**Edit WSGI configuration file:**
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/FTC'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'FTC.settings'

# Activate virtual environment
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Configure Static Files
In Web tab, add static file mappings:
- URL: `/static/` → Directory: `/home/yourusername/FTC/staticfiles`
- URL: `/media/` → Directory: `/home/yourusername/FTC/media`

### Step 7: Update settings.py
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
DEBUG = False

# Static files
STATIC_ROOT = '/home/yourusername/FTC/staticfiles'
MEDIA_ROOT = '/home/yourusername/FTC/media'
```

### Step 8: Reload Web App
Click "Reload yourusername.pythonanywhere.com" button

Your site will be live at: `https://yourusername.pythonanywhere.com`

---

## Cloud Deployment (Heroku)

### Prerequisites
- Heroku account ([https://heroku.com](https://heroku.com))
- Heroku CLI installed

### Step 1: Prepare Project Files

**Create `Procfile`** (in project root):
```
web: gunicorn FTC.wsgi --log-file -
```

**Create `runtime.txt`**:
```
python-3.12.10
```

**Update `requirements.txt`**:
```
Django==5.2.7
Pillow==10.4.0
mysqlclient
gunicorn
whitenoise
dj-database-url
python-decouple
```

### Step 2: Install Additional Dependencies
```bash
pip install gunicorn whitenoise dj-database-url python-decouple
pip freeze > requirements.txt
```

### Step 3: Update settings.py for Heroku
```python
import dj_database_url
from decouple import config

# Heroku settings
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'localhost']

# WhiteNoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database - use Heroku's database URL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
```

### Step 4: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-ftc-app-name

# Add MySQL addon (ClearDB)
heroku addons:create cleardb:ignite

# Get database URL
heroku config:get CLEARDB_DATABASE_URL

# Set config vars
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit for deployment"

# Deploy to Heroku
git push heroku master

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# Open your app
heroku open
```

---

## Cloud Deployment (AWS EC2)

### Step 1: Launch EC2 Instance
1. Go to AWS Console → EC2
2. Launch new instance (Ubuntu 22.04 LTS)
3. Choose t2.micro (free tier)
4. Configure security group:
   - SSH (22) - Your IP
   - HTTP (80) - Anywhere
   - HTTPS (443) - Anywhere
   - Custom TCP (8000) - Anywhere (for testing)
5. Download key pair (.pem file)

### Step 2: Connect to EC2
```bash
# Windows (PowerShell)
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

# Or use PuTTY on Windows
```

### Step 3: Setup Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx mysql-server -y

# Install MySQL client library
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y

# Create project directory
cd /home/ubuntu
mkdir ftc-project
cd ftc-project
```

### Step 4: Upload Project
```bash
# On your local machine
scp -i "your-key.pem" -r "c:\Users\HP.CHARANNEERUKOND\OneDrive\Desktop\FTC" ubuntu@your-ec2-ip:/home/ubuntu/ftc-project/
```

### Step 5: Setup Virtual Environment
```bash
# On EC2 instance
cd /home/ubuntu/ftc-project/FTC
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 6: Configure MySQL
```bash
sudo mysql
```
```sql
CREATE DATABASE ftc;
CREATE USER 'ftcuser'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON ftc.* TO 'ftcuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 7: Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Step 8: Configure Gunicorn
**Create systemd service file:**
```bash
sudo nano /etc/systemd/system/ftc.service
```

**Add content:**
```ini
[Unit]
Description=FTC Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ftc-project/FTC
Environment="PATH=/home/ubuntu/ftc-project/FTC/venv/bin"
ExecStart=/home/ubuntu/ftc-project/FTC/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/ftc-project/FTC/ftc.sock FTC.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl start ftc
sudo systemctl enable ftc
```

### Step 9: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/ftc
```

**Add content:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/ftc-project/FTC;
    }
    
    location /media/ {
        root /home/ubuntu/ftc-project/FTC;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/ftc-project/FTC/ftc.sock;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/ftc /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## Cloud Deployment (DigitalOcean)

### Step 1: Create Droplet
1. Go to DigitalOcean → Create → Droplets
2. Choose Ubuntu 22.04
3. Select Basic plan ($6/month)
4. Add SSH key
5. Create Droplet

### Step 2: Follow AWS EC2 Steps
The setup is nearly identical to AWS EC2 (Steps 2-9 above)

---

## Database Migration

### Export from Local MySQL
```bash
# On your local machine (Windows)
cd C:\xampp\mysql\bin
.\mysqldump.exe -u root -p ftc > ftc_backup.sql
```

### Import to Production MySQL

**PythonAnywhere:**
```bash
mysql -u yourusername -p yourusername$ftc < ftc_backup.sql
```

**AWS/DigitalOcean:**
```bash
mysql -u ftcuser -p ftc < ftc_backup.sql
```

---

## Post-Deployment Checklist

### ✅ Security Checklist
- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database credentials secured
- [ ] HTTPS enabled (SSL certificate)
- [ ] Firewall configured
- [ ] Regular backups scheduled

### ✅ Performance Checklist
- [ ] Static files collected and served properly
- [ ] Database indexed properly
- [ ] Caching enabled (Redis/Memcached)
- [ ] CDN configured for static files (optional)
- [ ] Database connection pooling
- [ ] Gunicorn workers optimized

### ✅ Functionality Checklist
- [ ] All pages load correctly
- [ ] Login/logout works
- [ ] Product listing works
- [ ] Add to cart works
- [ ] Cart view/delete works
- [ ] Checkout process works
- [ ] Admin panel accessible
- [ ] Image uploads work
- [ ] Email notifications work (if configured)

### ✅ Monitoring Setup
- [ ] Error logging configured
- [ ] Performance monitoring (e.g., New Relic, Sentry)
- [ ] Uptime monitoring
- [ ] Database backup automation

---

## Quick Commands Reference

### Django Commands
```bash
# Collect static files
python manage.py collectstatic --noinput

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Check deployment readiness
python manage.py check --deploy
```

### Gunicorn Commands
```bash
# Start Gunicorn
gunicorn FTC.wsgi:application --bind 0.0.0.0:8000

# With workers
gunicorn FTC.wsgi:application --workers 3 --bind 0.0.0.0:8000

# Check status (systemd)
sudo systemctl status ftc
sudo systemctl restart ftc
```

### Nginx Commands
```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# View logs
sudo tail -f /var/log/nginx/error.log
```

---

## Troubleshooting

### Common Issues

**1. Static files not loading**
```bash
# Run collectstatic
python manage.py collectstatic --noinput

# Check STATIC_ROOT setting
# Verify Nginx/Apache configuration
```

**2. Database connection error**
```python
# Verify database settings in settings.py
# Check MySQL is running
# Verify credentials
```

**3. Permission denied errors**
```bash
# Fix ownership
sudo chown -R ubuntu:www-data /home/ubuntu/ftc-project/FTC
sudo chmod -R 755 /home/ubuntu/ftc-project/FTC
```

**4. 502 Bad Gateway**
```bash
# Check Gunicorn is running
sudo systemctl status ftc

# Check socket file exists
ls -l /home/ubuntu/ftc-project/FTC/ftc.sock

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## 🎉 Recommended: Start with PythonAnywhere

For your first deployment, I recommend **PythonAnywhere** because:
- ✅ Free tier available
- ✅ MySQL included
- ✅ Easy web interface
- ✅ No server management needed
- ✅ Quick setup (30 minutes)
- ✅ Great for learning deployment

**Quick Start:**
1. Sign up at pythonanywhere.com
2. Upload your project
3. Create MySQL database
4. Configure WSGI file
5. Your site is live!

---

## Need Help?

- Django Deployment Docs: https://docs.djangoproject.com/en/5.2/howto/deployment/
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Heroku Django Guide: https://devcenter.heroku.com/articles/django-app-configuration
- DigitalOcean Tutorials: https://www.digitalocean.com/community/tags/django

---

**Good luck with your deployment! 🚀**
