# Database Management Guide

## Current Database Setup
- **Type**: SQLite Database
- **File**: `db.sqlite3` (25+ tables)
- **Status**: ✅ Active with complete product data

## Available Management Tools

### 1. Django Admin Interface
- **URL**: http://127.0.0.1:8000/admin/
- **Features**: Complete admin control, user management, product management
- **Access**: Admin credentials required

### 2. Database Dashboard  
- **URL**: http://127.0.0.1:8000/database-dashboard/
- **Features**: Real-time database statistics, table information
- **Access**: Available when Django server running

### 3. XAMPP phpMyAdmin
- **Setup**: Run `start_xampp_database.bat`
- **URL**: http://localhost/phpmyadmin (after XAMPP started)
- **Features**: Direct SQL queries, database backup/restore
- **Ports**: MySQL 3307, Apache 80 (to avoid conflicts)

## Database Content
- **Products**: Complete catalog with images and descriptions
- **Categories**: Aquaculture, Poultry, Meat categories
- **Orders**: Full order management system
- **Users**: Customer and admin accounts
- **Images**: Product images stored in media directory

## Backup Information
- Database file: `db.sqlite3`
- SQL backup: `FTC.sql` 
- Media files: `media/` directory
- Regular backups recommended before major changes