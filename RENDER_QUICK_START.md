# 🚀 Render Deployment - Quick Start Card

## ✅ Files Ready
- `requirements.txt` - Dependencies configured
- `build.sh` - Build script created
- `settings.py` - PostgreSQL support added
- `.gitignore` - Git ignore rules set

## 📋 Deployment Checklist

### Step 1: GitHub Setup (10 min)
```bash
cd "c:\Users\HP.CHARANNEERUKOND\OneDrive\Desktop\FTC"
git init
git add .
git commit -m "Initial commit"
# Create repo at github.com/new
git remote add origin https://github.com/YOUR_USERNAME/FTC.git
git push -u origin main
```

### Step 2: Render Database (5 min)
1. Go to [render.com/dashboard](https://dashboard.render.com)
2. New + → PostgreSQL
3. Name: `ftc-database`, Free tier
4. Copy **Internal Database URL**

### Step 3: Render Web Service (5 min)
1. New + → Web Service
2. Connect GitHub repo
3. Settings:
   - **Build**: `./build.sh`
   - **Start**: `gunicorn FTC.wsgi:application`
   - **Plan**: Free

### Step 4: Environment Variables (5 min)
Add in "Advanced" section:
```
PYTHON_VERSION = 3.12.10
DATABASE_URL = (paste from Step 2)
SECRET_KEY = (generate new - see below)
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
```

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy! (10 min)
Click "Create Web Service" - Wait for build to complete

### Step 6: Create Superuser (2 min)
In Render Shell tab:
```bash
python manage.py createsuperuser
```

## 🎉 Your App is Live!
- **URL**: https://your-app-name.onrender.com
- **Admin**: https://your-app-name.onrender.com/admin

## 🔄 Update App
```bash
git add .
git commit -m "Update message"
git push origin main
# Render auto-deploys!
```

## ⏱️ Total Time: ~30-40 minutes

## 📖 Full Guide
See `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions

## 🆘 Need Help?
- Logs: Render Dashboard → Your Service → Logs
- Docs: [render.com/docs](https://render.com/docs)
