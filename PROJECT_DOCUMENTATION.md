# FTC Agricultural Marketplace - Setup Documentation

## Email Configuration Guide

### Gmail SMTP Setup
1. Use Gmail App Password: `pdafomlequfxcgbn` 
2. Email configured in settings.py for charanneerukonda7@gmail.com
3. Order notifications automatically sent to customers and admin

### Email Testing
- Test emails via: http://127.0.0.1:8000/products/test-email/
- Check spam folder if emails not received
- All order confirmations sent automatically

## Database Information

### Current Database: SQLite
- File: `db.sqlite3`
- Contains 25+ tables with complete product data
- Order management system active
- User authentication working

### Database Management
- Django Admin: http://127.0.0.1:8000/admin/
- Database Dashboard: http://127.0.0.1:8000/database-dashboard/
- XAMPP phpMyAdmin: Run `start_xampp_database.bat`

## Product Categories
- **Aquaculture**: Fresh Fish (Catla, Rohu, Mud Crab)
- **Poultry**: Chicken products and Eggs  
- **Meat**: Mutton and other meat products
- **Processed**: Value-added products

## Order Management
- Complete order processing system
- Email notifications for order status
- Admin interface for order management
- Order history and tracking

## Mobile Optimization (Removed for Laptop-Only)
- All mobile-specific code removed as requested
- Focus on laptop/desktop experience
- Simplified codebase for laptop usage

## Key Features Working
✅ Product catalog with images
✅ Order management system  
✅ Email notifications (Gmail SMTP)
✅ User registration/login
✅ Admin interface
✅ Database management tools
✅ Static file serving