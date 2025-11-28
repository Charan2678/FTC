# Email System Configuration

## Current Working Setup
- **Gmail SMTP**: smtp.gmail.com:587
- **Username**: charanneerukonda7@gmail.com  
- **App Password**: pdafomlequfxcgbn
- **Status**: ✅ WORKING - Real emails being sent

## Email Notifications Active
- Order confirmations sent to customers
- Admin notifications for new orders
- Order status updates
- Test emails available via admin interface

## Gmail App Password Setup (Already Done)
1. Google Account → Security → 2-Step Verification (Enabled)
2. App Passwords → Generated: `pdafomlequfxcgbn`
3. Django settings.py configured with working credentials

## Testing Email System
```python
# Test via Django admin or direct URL:
http://127.0.0.1:8000/admin/
# Look for email test options in admin interface
```

## Troubleshooting
- Check spam/junk folders for test emails
- Gmail App Password is working (confirmed)
- SMTP settings correctly configured in settings.py
- No firewall blocking required for email (SMTP uses standard ports)