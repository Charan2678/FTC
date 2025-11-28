from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def email_diagnostic_view(request):
    """Simple email diagnostic and testing"""
    if request.method == 'POST':
        try:
            # Send test email
            subject = 'FTC Test Email'
            message = 'This is a test email from FTC Agricultural Marketplace.\n\nIf you receive this, your email system is working correctly!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.ADMIN_EMAIL]
            
            send_mail(subject, message, from_email, recipient_list)
            
            return JsonResponse({
                'success': True,
                'message': 'Test email sent successfully!',
                'details': f'Email sent to {settings.ADMIN_EMAIL}. Check inbox and spam folder.'
            })
            
        except Exception as e:
            logger.error(f'Email test failed: {e}')
            return JsonResponse({
                'success': False,
                'message': f'Email test failed: {str(e)}',
                'details': 'Check Gmail App Password and SMTP settings in Django configuration.'
            })
    
    # GET request - show diagnostic page
    email_config = {
        'backend': settings.EMAIL_BACKEND,
        'host': settings.EMAIL_HOST,
        'port': settings.EMAIL_PORT,
        'use_tls': settings.EMAIL_USE_TLS,
        'username': settings.EMAIL_HOST_USER,
        'password_configured': bool(settings.EMAIL_HOST_PASSWORD),
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'admin_email': settings.ADMIN_EMAIL
    }
    
    return render(request, 'email_diagnostic.html', {'config': email_config})