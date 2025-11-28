# 🚀 Deploy FTC Django Project to Render

## Overview
Render is a modern cloud platform that makes deploying web applications easy. It offers:
- ✅ **Free tier** with PostgreSQL database
- ✅ Automatic HTTPS/SSL certificates
- ✅ Git-based deployments
- ✅ Easy setup (30-45 minutes)
- ✅ Better than Heroku's free tier

---

## Prerequisites

### 1. Create Accounts
- **GitHub Account**: [github.com](https://github.com) (for code hosting)
- **Render Account**: [render.com](https://render.com) (for deployment)

### 2. Install Git
If you don't have Git installed:
```bash
# Download from: https://git-scm.com/download/win
# Or use: winget install Git.Git
```

---

## Step 1: Prepare Your Project

### Files Already Created ✅
I've already created these files for you:
- ✅ `requirements.txt` - Python dependencies
- ✅ `build.sh` - Build script for Render
- ✅ `settings.py` - Updated with PostgreSQL support

### Verify Files Created
```bash
cd "c:\Users\HP.CHARANNEERUKOND\OneDrive\Desktop\FTC"
dir requirements.txt
dir build.sh
```

---

## Step 2: Push to GitHub

### Initialize Git Repository
```bash
cd "c:\Users\HP.CHARANNEERUKOND\OneDrive\Desktop\FTC"

# Initialize git (if not already done)
git init

# Create .gitignore file
```

### Create `.gitignore` file
Create a file named `.gitignore` in your project root with this content:

```
# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
staticfiles/
media/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Sensitive data
*.pem
*.key
```

### Commit and Push
```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for Render deployment"

# Create repository on GitHub (go to github.com/new)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/FTC.git
git branch -M main
git push -u origin main
```

---

## Step 3: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)

2. **Create Database**:
   - Click "New +" button
   - Select "PostgreSQL"
   - Fill in details:
     - **Name**: `ftc-database`
     - **Database**: `ftc`
     - **User**: (auto-generated)
     - **Region**: Choose closest to you
     - **Plan**: Free
   - Click "Create Database"

3. **Save Database Info**:
   - Wait for database to provision (2-3 minutes)
   - Copy the **Internal Database URL** (starts with `postgresql://`)
   - Keep this tab open - you'll need it!

---

## Step 4: Create Web Service on Render

### Create New Web Service

1. **Click "New +" → "Web Service"**

2. **Connect GitHub**:
   - Connect your GitHub account
   - Select your FTC repository
   - Click "Connect"

3. **Configure Service**:

   **Basic Settings:**
   - **Name**: `ftc-app` (or your preferred name)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`

   **Build & Deploy:**
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn FTC.wsgi:application`

   **Plan:**
   - Select "Free"

### Add Environment Variables

Click "Advanced" and add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.10` |
| `DATABASE_URL` | (Paste Internal Database URL from Step 3) |
| `SECRET_KEY` | (Generate a new secret key - see below) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `ftc-app.onrender.com` (replace with your app name) |

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Deploy!

4. **Click "Create Web Service"**

   Render will now:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your app

   This takes **5-10 minutes** for the first deployment.

---

## Step 5: Monitor Deployment

### Check Logs
1. Go to your web service dashboard
2. Click "Logs" tab
3. Watch for:
   - ✅ `Installing dependencies...`
   - ✅ `Running migrations...`
   - ✅ `Collecting static files...`
   - ✅ `Starting gunicorn...`
   - ✅ `Listening at: http://0.0.0.0:10000`

### Common Issues

**Issue 1: Build fails with "No module named 'decouple'"**
```bash
# Add to requirements.txt:
python-decouple==3.8
```

**Issue 2: Static files not loading**
```bash
# In settings.py, verify:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Issue 3: Database connection error**
- Verify DATABASE_URL is correct
- Check database is running in Render dashboard

---

## Step 6: Create Superuser

After successful deployment:

1. **Go to Shell Tab** in your web service
2. **Run command**:
```bash
python manage.py createsuperuser
```
3. Enter username, email, and password
4. Access admin at: `https://your-app.onrender.com/admin`

---

## Step 7: Test Your Application

### Test Basic Functionality
- ✅ Homepage loads: `https://your-app.onrender.com/`
- ✅ Products page works
- ✅ Add to cart works
- ✅ Cart listing works
- ✅ Admin panel: `https://your-app.onrender.com/admin`

### Test Database
1. Login to admin panel
2. Add a product
3. View product on frontend
4. Add to cart
5. Check cart

---

## Step 8: Import Your MySQL Data (Optional)

If you want to migrate existing data from MySQL to PostgreSQL:

### Method 1: Using Django Fixtures

**Export from MySQL (Local):**
```bash
# In your local environment
python manage.py dumpdata products > products_data.json
python manage.py dumpdata company > company_data.json
python manage.py dumpdata users > users_data.json
```

**Import to PostgreSQL (Render Shell):**
```bash
# In Render Shell tab
python manage.py loaddata products_data.json
python manage.py loaddata company_data.json
python manage.py loaddata users_data.json
```

### Method 2: Manual Migration
1. Export MySQL data to CSV
2. Use pgAdmin to import to PostgreSQL
3. Or use Django admin to manually add data

---

## Render Configuration Summary

### Your Render URLs
- **App URL**: `https://ftc-app.onrender.com` (replace with your name)
- **Admin URL**: `https://ftc-app.onrender.com/admin`
- **Database**: Internal PostgreSQL (managed by Render)

### Free Tier Limits
- ✅ Web Service: Free (spins down after 15 min inactivity)
- ✅ PostgreSQL: 256 MB storage, 100 connections
- ✅ Bandwidth: 100 GB/month
- ✅ Build minutes: 500/month
- ❌ No custom domain on free tier (use .onrender.com)

### Automatic Features
- ✅ HTTPS/SSL certificates
- ✅ Automatic deploys on git push
- ✅ Health checks
- ✅ Log persistence (7 days)

---

## Updating Your App

### Deploy New Changes

```bash
# Make changes to your code
# Commit and push:
git add .
git commit -m "Updated feature X"
git push origin main
```

Render will automatically:
1. Detect the push
2. Build your app
3. Run migrations
4. Deploy new version

---

## Production Checklist

Before going live:

### Security ✅
- [ ] `DEBUG = False` in environment variables
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database credentials secure
- [ ] HTTPS enabled (automatic on Render)

### Functionality ✅
- [ ] All pages load correctly
- [ ] Login/logout works
- [ ] Product CRUD works
- [ ] Cart functionality works
- [ ] Order processing works
- [ ] Admin panel accessible
- [ ] Images display correctly

### Performance ✅
- [ ] Static files served via WhiteNoise
- [ ] Database queries optimized
- [ ] Images optimized (compressed)
- [ ] Browser caching enabled

---

## Troubleshooting

### App Not Loading

**Check Logs:**
```
Render Dashboard → Your Service → Logs
```

**Common Fixes:**
1. Verify `build.sh` has execution permissions
2. Check all environment variables are set
3. Verify `ALLOWED_HOSTS` includes your Render URL
4. Check database connection

### Static Files Not Loading

**Solution:**
1. Verify WhiteNoise is in MIDDLEWARE (line 2)
2. Run collectstatic in build.sh
3. Check STATICFILES_STORAGE setting

### Database Connection Error

**Solution:**
1. Verify DATABASE_URL environment variable
2. Check database is "Available" in Render dashboard
3. Ensure psycopg2-binary is in requirements.txt

### Build Fails

**Solution:**
1. Check Python version matches (3.12.10)
2. Verify all dependencies in requirements.txt
3. Check build.sh syntax (Unix line endings)

---

## Cost Breakdown

### Free Tier (Perfect for Testing)
- ✅ Free web service (with sleep after inactivity)
- ✅ Free PostgreSQL database (256 MB)
- ✅ Perfect for learning and demos

### Paid Tier (Production Ready)
- 💰 **Starter Plan**: $7/month
  - No sleep
  - Always-on
  - 512 MB RAM
  - Custom domain support

- 💰 **PostgreSQL**: $7/month (1 GB)
  - Daily backups
  - Point-in-time recovery

**Total for Production**: ~$14/month

---

## Advantages of Render

### vs PythonAnywhere:
- ✅ Better free tier (no daily restart)
- ✅ Automatic HTTPS
- ✅ Git-based deployment
- ✅ Modern dashboard

### vs Heroku:
- ✅ Better free tier
- ✅ Free PostgreSQL included
- ✅ Easier setup
- ✅ Lower paid tier costs

### vs AWS EC2:
- ✅ Much simpler setup
- ✅ No server management
- ✅ Automatic scaling
- ✅ Built-in monitoring

---

## Next Steps After Deployment

1. **Add Custom Domain** (Paid tier only):
   - Buy domain (Namecheap, GoDaddy)
   - Add to Render dashboard
   - Update DNS records

2. **Setup Monitoring**:
   - Enable Render health checks
   - Add Sentry for error tracking
   - Setup uptime monitoring

3. **Optimize Performance**:
   - Add Redis for caching
   - Use CDN for static files
   - Optimize database queries

4. **Backup Strategy**:
   - Enable Render database backups (paid)
   - Export data regularly
   - Test restore procedures

---

## Support Resources

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Django Deployment**: [docs.djangoproject.com/en/5.2/howto/deployment/](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- **Render Community**: [community.render.com](https://community.render.com)
- **Django Forum**: [forum.djangoproject.com](https://forum.djangoproject.com)

---

## Quick Reference Commands

### Local Development
```bash
# Run locally
python manage.py runserver

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Git Commands
```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to trigger deployment
git push origin main
```

### Render Shell Commands
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Check logs
# (Use Render dashboard Logs tab)
```

---

## 🎉 You're Ready to Deploy!

Follow the steps in order:
1. ✅ Files prepared (done)
2. Push to GitHub
3. Create PostgreSQL database
4. Create web service
5. Configure environment variables
6. Deploy!

**Your app will be live at**: `https://your-app-name.onrender.com`

Good luck! 🚀
