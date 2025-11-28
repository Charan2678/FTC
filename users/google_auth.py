"""
Google OAuth Authentication Handler for FTC Platform
Handles Google Sign-In for both login and signup
"""

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from users.models import user as User
import secrets


def verify_google_token(token):
    """
    Verify Google ID token and return user info
    """
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            settings.GOOGLE_OAUTH_CLIENT_ID
        )

        # Verify the issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # Token is valid, return user info
        return {
            'google_id': idinfo['sub'],
            'email': idinfo['email'],
            'name': idinfo.get('name', ''),
            'picture': idinfo.get('picture', ''),
            'email_verified': idinfo.get('email_verified', False)
        }
    except ValueError as e:
        print(f"Token verification failed: {str(e)}")
        return None


def get_or_create_google_user(google_user_info):
    """
    Get existing user or create new user from Google info
    Returns: (user_object, created_boolean)
    """
    try:
        # Try to find existing user by email
        existing_user = User.objects.filter(user_email=google_user_info['email']).first()
        
        if existing_user:
            # User exists, return it
            return existing_user, False
        
        # Create new user
        username = google_user_info['email'].split('@')[0]
        
        # Make sure username is unique
        base_username = username
        counter = 1
        while User.objects.filter(user_username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Generate random password (user won't need it for Google login)
        random_password = secrets.token_urlsafe(16)
        
        new_user = User(
            user_name=google_user_info['name'],
            user_username=username,
            user_email=google_user_info['email'],
            user_password=random_password,
            user_mobile='',
            user_gender='',
            user_dob='',
            user_add1='',
            user_add2='',
            user_city='0',
            user_state='0',
            user_country='0',
            user_level_id='2',  # Default: Customer
            user_image=google_user_info.get('picture', '')
        )
        new_user.save()
        
        return new_user, True
        
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return None, False


def handle_google_login(request, token):
    """
    Handle Google OAuth login process
    """
    # Verify the Google token
    google_user_info = verify_google_token(token)
    
    if not google_user_info:
        messages.error(request, "Google authentication failed. Please try again.")
        return redirect('/users/')
    
    if not google_user_info['email_verified']:
        messages.error(request, "Please verify your email with Google first.")
        return redirect('/users/')
    
    # Get or create user
    user_obj, created = get_or_create_google_user(google_user_info)
    
    if not user_obj:
        messages.error(request, "Failed to create user account. Please try again.")
        return redirect('/users/')
    
    # Set session (log the user in)
    request.session['authenticated'] = True
    request.session['user_id'] = user_obj.user_id
    request.session['user_level_id'] = user_obj.user_level_id
    request.session['user_name'] = user_obj.user_name
    request.session['user_email'] = user_obj.user_email
    request.session['order_id'] = "0"
    
    if created:
        messages.success(request, f"Welcome {user_obj.user_name}! Your account has been created successfully.")
    else:
        messages.success(request, f"Welcome back, {user_obj.user_name}!")
    
    # Redirect based on user level
    if user_obj.user_level_id == '1':  # Admin
        return redirect('/users/dashboard')
    else:  # Customer
        return redirect('/')
