# FTC Agricultural Marketplace

## Project Overview
A Django-based agricultural marketplace for fresh products including fish, poultry, meat, and eggs with order management and email notifications.

## Quick Start
1. Double-click `start_ftc_laptop.bat` to start the application
2. Access at: http://127.0.0.1:8000/
3. Admin panel: http://127.0.0.1:8000/admin/

## ✅ Current Working Features
- **Product Catalog**: Complete with categories (Fish, Poultry, Meat, Eggs)
- **Order Management**: Full order processing system with status tracking
- **Email Notifications**: Gmail SMTP working with App Password
- **User System**: Registration, login, customer accounts
- **Admin Interface**: Complete Django admin for management
- **Database Tools**: Multiple database management interfaces
- **Email Testing**: http://127.0.0.1:8000/products/test-email/

## 🗄️ Database Management
- **Django Admin**: http://127.0.0.1:8000/admin/
- **Database Dashboard**: http://127.0.0.1:8000/database-dashboard/
- **XAMPP phpMyAdmin**: Run `start_xampp_database.bat`
- **Current DB**: SQLite with 25+ tables

## 📧 Email System (WORKING)
- **Gmail SMTP**: charanneerukonda7@gmail.com
- **App Password**: pdafomlequfxcgbn (configured)
- **Auto Notifications**: Order confirmations, status updates
- **Test Interface**: Available in admin and products section

## 🧹 Cleanup Performed
- **Removed**: Mobile-specific code (as requested)
- **Removed**: Unnecessary documentation files
- **Removed**: Diagram files (.drawio)
- **Removed**: Old development scripts
- **Kept**: All core functionality and working features
- **Restored**: Essential email testing and diagnostics

## Key Components
- **Django 5.2.7** - Web framework
- **SQLite** - Database (db.sqlite3)
- **Gmail SMTP** - Email notifications (working)
- **Bootstrap** - Frontend styling

## File Structure
```
FTC/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── start_ftc_laptop.bat     # Application launcher
├── db.sqlite3               # SQLite database
├── FTC/                     # Main Django app
├── pages/                   # Homepage and static pages
├── products/                # Product management
├── users/                   # User authentication
├── company/                 # Company information
├── type/                    # Product categories
├── templates/               # HTML templates
├── assets/                  # CSS, JS, images
└── media/                   # Uploaded files
```

## Management Scripts
- `start_ftc_laptop.bat` - Start the application
- `start_xampp_database.bat` - Database management tools
- `quick_database_access.bat` - Quick database access
- `restart_xampp.bat` - XAMPP server management
- `stop_xampp.bat` - Stop XAMPP services