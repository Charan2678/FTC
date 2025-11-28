from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email as django_validate_email
from .models import role, user, city, state, country

# Simple security functions
def sanitize_input(value):
    return str(value).strip() if value else ''

def hash_password(password):
    return make_password(password)

def verify_password(password, hashed_password):
    return check_password(password, hashed_password)

def validate_password_strength(password):
    if len(password) < 6:
        raise ValidationError('Password must be at least 6 characters long')
    return True

def validate_email(email):
    django_validate_email(email)
    return True

def validate_mobile(mobile):
    if not mobile.isdigit() or len(mobile) < 10:
        raise ValidationError('Mobile number must be at least 10 digits')
    return True

# Create your views here.
@csrf_protect
def index(request):
    if(request.session.get('authenticated', False) == True):
        return redirect('/users/dashboard')

    context = {
        "message": "Please Log in",
        "error": False
    }
   
    if(request.method == "POST"):
        try:
            # Get raw input (don't sanitize username/password for debugging)
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            
            if not username or not password:
                context['message'] = "Username and password are required"
                context['error'] = True
                return render(request,'login.html', context)
            
            # Debug print
            print(f"Login attempt - Username: '{username}', Password length: {len(password)}")
            
            getUser = user.objects.get(user_username=username)
            print(f"User found - DB Username: '{getUser.user_username}', DB Password: '{getUser.user_password}'")
            context['msg'] = getUser
        except user.DoesNotExist:
            print(f"User not found for username: '{username}'")
            context['message'] = "Invalid credentials"
            context['error'] = True
            return render(request,'login.html', context)
        except Exception as e:
            print(f"Login exception: {str(e)}")
            context['message'] = "Login error occurred"
            context['error'] = True
            return render(request,'login.html', context)
            
        # Check password - support both old plain text and new hashed passwords
        password_valid = False
        
        # Try new hashed password verification first
        try:
            if getUser.user_password.startswith('pbkdf2_') or getUser.user_password.startswith('argon2'):
                password_valid = verify_password(password, getUser.user_password)
            else:
                # Fallback to plain text comparison for existing users
                password_valid = (getUser.user_password == password)
                
                # If login successful with plain text, upgrade to hashed password
                if password_valid:
                    getUser.user_password = hash_password(password)
                    getUser.save()
        except Exception as e:
            # If hash verification fails, try plain text
            password_valid = (getUser.user_password == password)
        
        if password_valid:
            request.session['authenticated'] = True
            request.session['user_id'] = getUser.user_id
            request.session['user_level_id'] = getUser.user_level_id
            request.session['user_name'] = getUser.user_name
            # Add session security
            request.session.cycle_key()
            return redirect('/users/dashboard')
        else:
            context['message'] = "Invalid credentials"
            context['error'] = True
            return render(request,'login.html', context)
    else:
        return render(request,'login.html', context)

def listing(request, userId=None):
    if(request.session.get('authenticated', False) != True):
        return redirect('/')
    
    # If no userId provided, show all users or redirect based on user level
    if userId is None:
        user_level = request.session.get('user_level_id', 2)
        if user_level == 1:  # Admin can see all users
            userlist = user.objects.all()
            context = {
                "showmsg": True,
                "message": "All Users Report",
                "userlist": userlist,
                "heading": "All Users Report"
            }
        else:
            # Regular users see their own info
            return redirect('/users/dashboard')
    else:
        try:
            userlist =  user.objects.filter(Q(user_level_id=userId))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context = {
            "showmsg": True,
            "message": "User Updated Successfully",
            "userlist": userlist
        }
        # Message according Users Role #
        if(userId == "1"):
            context['heading'] = "System Admin Report";
        if(userId == "2"):
            context['heading'] = "Consumer User Report";
        # if(userId == "3"):
        #     context['heading'] = "Doctors Report";
        # if(userId == "4"):
        #     context['heading'] = "Patient Report";
    return render(request,'user-report.html',context)

def dashboard(request):
    return render(request,'dashboard.html')

def forgot(request):
    return render(request,'forgotpass.html')

def update(request, userId):
    context = {
    "fn":"update",
    "citylist":city.objects.all(),
    "statelist":state.objects.all(),
    "rolelist":role.objects.all(),
    "countrylist":country.objects.all(),
    "userdetails":user.objects.get(user_id=userId)
    }
    currentUserDetails = user.objects.get(user_id = userId)
    context['sub_heading'] = "Update Details of "+currentUserDetails.user_name;
    # Message according Users Role #
    if(currentUserDetails.user_level_id == 1):
        context['heading'] = "System Admin Management";
    if(currentUserDetails.user_level_id == 2):
        context['heading'] = "Consumer User Management";
    # if(currentUserDetails.user_level_id == 3):
    #     context['heading'] = "Doctors Management";
    # if(currentUserDetails.user_level_id == 4):
    #     context['heading'] = "Patient Management";

    if (request.method == "POST"):
        
        try:
            user_image = None
            user_image = currentUserDetails.user_image
            if(request.FILES and request.FILES['user_image']):
                userImage = request.FILES['user_image']
                fs = FileSystemStorage()
                filename = fs.save(userImage.name, userImage)
                user_image = fs.url(userImage)
            
            addUser = user(
            user_id = userId,
            user_name = request.POST['user_name'],
            user_username = request.POST['user_username'],
            user_email = request.POST['user_email'],
            user_password = request.POST['user_password'],
            user_mobile = request.POST['user_mobile'],
            user_gender = request.POST['user_gender'],
            user_dob = request.POST['user_dob'],
            user_add1 = request.POST['user_add1'],
            user_add2 = request.POST['user_add2'],
            user_city = request.POST['user_city'],
            user_country = request.POST['user_country'],
            user_state = request.POST['user_state'],
            user_image = user_image)
            
            addUser.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        # if (request.session.get('user_level_id', None) == 1):    
        #     messages.add_message(request, messages.INFO, "User Updated Successfully !!!")
        #     return redirect('/users/report/'+request.POST['user_level_id'])
    
        context["userdetails"] = user.objects.get(user_id=userId)
        messages.add_message(request, messages.INFO, "Your Account Updated Successfully !!!")
        return render(request,'user.html', context)
    else:
        return render(request,'user.html', context)

@csrf_protect
def add(request):
    context = {
    "fn":"add",
    "citylist":city.objects.all(),
    "rolelist":role.objects.all(),
    "heading":'Users Management',
    "sub_heading": 'Users',
    "statelist":state.objects.all(),
    "countrylist":country.objects.all(),
    "error_messages": []
    }
    context['heading'] = "Customer Registration";
    context['sub_heading'] = "Register to Account";
    
    if (request.method == "POST"):
        try:
            # Input validation and sanitization
            user_name = sanitize_input(request.POST.get('user_name', ''))
            user_username = sanitize_input(request.POST.get('user_username', ''))
            user_email = sanitize_input(request.POST.get('user_email', ''))
            user_password = request.POST.get('user_password', '')
            user_mobile = sanitize_input(request.POST.get('user_mobile', ''))
            
            # Validate required fields
            if not all([user_name, user_username, user_email, user_password]):
                context['error_messages'].append("All required fields must be filled")
                return render(request,'signup.html', context)
            
            # Validate password strength
            try:
                validate_password_strength(user_password)
            except ValidationError as e:
                context['error_messages'].append(str(e))
                return render(request,'signup.html', context)
            
            # Validate email format
            try:
                validate_email(user_email)
            except ValidationError as e:
                context['error_messages'].append(str(e))
                return render(request,'signup.html', context)
            
            # Validate mobile if provided
            if user_mobile:
                try:
                    validate_mobile(user_mobile)
                except ValidationError as e:
                    context['error_messages'].append(str(e))
                    return render(request,'signup.html', context)
            
            # Check if username or email already exists
            if user.objects.filter(user_username=user_username).exists():
                context['error_messages'].append("Username already exists")
                return render(request,'signup.html', context)
                
            if user.objects.filter(user_email=user_email).exists():
                context['error_messages'].append("Email already registered")
                return render(request,'signup.html', context)

            user_image = None
            if(request.FILES and request.FILES.get('user_image')):
                userImage = request.FILES['user_image']
                fs = FileSystemStorage()
                filename = fs.save(userImage.name, userImage)
                user_image = fs.url(userImage)

            # Hash password before saving
            hashed_password = hash_password(user_password)

            addUser = user(
                user_name=user_name,
                user_username=user_username,
                user_email=user_email,
                user_password=hashed_password,
                user_mobile=user_mobile,
                user_gender=sanitize_input(request.POST.get('user_gender', '')),
                user_dob=request.POST.get('user_dob', None),
                user_add1=sanitize_input(request.POST.get('user_add1', '')),
                user_add2=sanitize_input(request.POST.get('user_add2', '')),
                user_city=sanitize_input(request.POST.get('user_city', '0')),
                user_country=sanitize_input(request.POST.get('user_country', '0')),
                user_state=sanitize_input(request.POST.get('user_state', '0')),
                user_level_id=request.POST.get('user_level_id', '2'),
                user_image=user_image
            )
            addUser.save()
            
        except Exception as e:
            context['error_messages'].append(f"Registration failed: {str(e)}")
            return render(request,'signup.html', context)
            
        messages.add_message(request, messages.SUCCESS, "Your account has been registered successfully. Login with your credentials !!!")
        return redirect('/users')

    else:
        return render(request,'signup.html', context)

def farmer_register(request):
    from company.models import company
    context = {
    "fn":"add_farmer",
    "citylist":city.objects.all(),
    "statelist":state.objects.all(),
    "countrylist":country.objects.all()
    }
    if (request.method == "POST"):
        try:
            user_image = None
            if(request.FILES and request.FILES.get('user_image')):
                userImage = request.FILES['user_image']
                fs = FileSystemStorage()
                filename = fs.save(userImage.name, userImage)
                user_image = fs.url(userImage)
            
            # Create user account
            addUser = user(
                user_name = request.POST['user_name'],
                user_username = request.POST['user_username'],
                user_email = request.POST['user_email'],
                user_password = request.POST['user_password'],
                user_mobile = request.POST['user_mobile'],
                user_gender = request.POST['user_gender'],
                user_dob = request.POST.get('user_dob', ''),
                user_add1 = request.POST.get('user_add1', ''),
                user_add2 = request.POST.get('user_add2', ''),
                user_city = request.POST['user_city'],
                user_country = request.POST['user_country'],
                user_state = request.POST['user_state'],
                user_level_id = 3,  # Farmer role
                user_image = user_image
            )
            addUser.save()
            
            # Create company record for the farmer
            if request.POST.get('company_name'):
                addCompany = company(
                    company_name = request.POST['company_name'],
                    company_address = request.POST.get('user_add1', '') + ', ' + request.POST.get('user_add2', ''),
                    company_contact = request.POST['user_mobile'],
                    company_email = request.POST['user_email']
                )
                addCompany.save()
                
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))
        messages.add_message(request, messages.INFO, "Your farmer account has been registered successfully. Login with your credentials !!!")
        return redirect('/users')
    else:
        return render(request,'farmer-register.html', context)

def logout(request):
    request.session['authenticated']= False
    request.session['user_id'] = False
    request.session['user_level_id']= False
    request.session['user_name']= False
    return redirect('/')

def changepassword(request):
    if (request.method == "POST"):
        try:
            addUser = user(
                user_id = request.session.get('user_id', None),
                user_password = request.POST['user_new_password']
            )
            addUser.save(update_fields=["user_password"])
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))
        messages.add_message(request, messages.INFO, "Your Password has been changed successfully !!!")
        return render(request,'change-password.html')

    else:
        return render(request,'change-password.html')
    return render(request,'change-password.html')

def delete(request, userId):
    try:
        deleteUser = user.objects.get(user_id = userId)
        deleteUser.delete()
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))
    messages.add_message(request, messages.INFO, "User Deleted Successfully !!!")
    return redirect('listing')


# Google OAuth Views
def google_login(request):
    """
    Initiate Google OAuth login
    """
    from django.conf import settings
    import urllib.parse
    
    # Check if Google OAuth is configured
    if not hasattr(settings, 'GOOGLE_OAUTH_CLIENT_ID'):
        messages.error(request, "Google Sign-In is not configured. Please contact administrator.")
        return redirect('/users/')
    
    # Build Google OAuth URL
    params = {
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'online',
    }
    
    google_auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
    return redirect(google_auth_url)


def google_callback(request):
    """
    Handle Google OAuth callback
    """
    from django.conf import settings
    import requests as http_requests
    
    # Get authorization code
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, "Google authentication failed. Please try again.")
        return redirect('/users/')
    
    # Exchange code for token
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    try:
        token_response = http_requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'id_token' in token_json:
            # Import and use Google auth handler
            from .google_auth import handle_google_login
            return handle_google_login(request, token_json['id_token'])
        else:
            messages.error(request, "Failed to authenticate with Google. Please try again.")
            return redirect('/users/')
            
    except Exception as e:
        print(f"Google OAuth Error: {str(e)}")
        messages.error(request, "An error occurred during Google sign-in. Please try again.")
        return redirect('/users/')
