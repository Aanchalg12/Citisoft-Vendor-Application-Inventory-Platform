from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from myCitisoft.forms import SignupForm
from django.db import models
from .models import CustomUser
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
auth = get_user_model()
from .forms import ProfileUpdateForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from .forms import AddUserForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

def user_list(request):
    users = CustomUser.objects.all()
    vendors = CustomUser.objects.filter(role='vendor').order_by('id').values('username', 'email', 'phone_number', 'address', 'id')
    reviewers = CustomUser.objects.filter(role='reviewer').order_by('id').values('username', 'email', 'phone_number', 'address', 'id')
    customers = CustomUser.objects.filter(role='customer').order_by('id').values('username', 'email', 'phone_number', 'address', 'id')

   # Paginate each queryset
    vendor_paginator = Paginator(vendors, 4)
    customer_paginator = Paginator(customers, 4)
    reviewer_paginator = Paginator(reviewers, 4)

    # Get the page number from the request
    vendor_page_number = request.GET.get('vendor_page')
    customer_page_number = request.GET.get('customer_page')
    reviewer_page_number = request.GET.get('reviewer_page')

    # Get the page objects for each paginator
    vendor_page_obj = vendor_paginator.get_page(vendor_page_number)
    customer_page_obj = customer_paginator.get_page(customer_page_number)
    reviewer_page_obj = reviewer_paginator.get_page(reviewer_page_number)

    return render(request, 'user_list.html', {'vendor_page_obj': vendor_page_obj, 'customer_page_obj': customer_page_obj, 'reviewer_page_obj': reviewer_page_obj})


def deleteuser(request):
    
    return render(request, 'deleteuser.html')

def viewprofile(request, user_id):
    # Retrieve the user object using the provided user_id
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'viewprofile.html', {'user': user})

def userprofile(request):
    user = request.user
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        profile = None

    print("Profile Object:", profile)
    if profile:
        print("Name:", profile.username)
        print("Email:", profile.email)
        print("Address:", profile.address)
        print("Phone Number:", profile.phone_number)

    if profile:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.instance.username = user.username
                 # Save only the fields that are filled in the form
                form.save(update_fields=form.changed_data)
                messages.success(request, 'User profile updated successfully.')
                return redirect('userprofile')
                # form.save() 
                # messages.success(request, 'Profile updated successfully')
                # return redirect('userprofile')
        else:
            # Pre-fill the form with existing profile data
            initial_data = {
                'username': profile.username,
                'email': profile.email,
                'address': profile.address,
                'phone_number': profile.phone_number,
                # Add more fields as needed
            }
            form = ProfileUpdateForm(instance=user, initial=initial_data)
    else:
        form = ProfileUpdateForm(instance=user)  # Create a new form instance if profile does not exist

    return render(request, 'userprofile.html', {'form': form})


def search_users(request):
    query = request.GET.get('query')
    if query:
        users = CustomUser.objects.filter(username__icontains=query)
    else:
        users = None

    return render(request, 'search_results.html', {'users': users, 'query': query})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Your account has been successfully created")
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()
    return render(request, 'Signup1.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            CustomUser = authenticate(username=username, password=password)
            if CustomUser is not None:
                login(request, CustomUser)
                return redirect('dashboard')  # Redirect to dashboard upon successful login
            else:
                form.add_error(None, "Invalid username or password")  # Add non-field error
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def dashboard(request):
    user = request.user
    context = {}  # Initialize context dictionary

    if user.is_authenticated:
        if user.role == 'admin':
            # Add context data for admin dashboard
            context['admin_data'] = {}  # Add admin-specific data as needed
            return render(request, "admindashboard.html", context)
        elif user.role == 'vendor':
            # Add context data for vendor dashboard
            context['vendor_data'] = {}  # Add vendor-specific data as needed
            return render(request, "vendordashboard.html", context)
        elif user.role == 'customer':
            # Add context data for customer dashboard
            context['customer_data'] = {}  # Add customer-specific data as needed
            return render(request, "customerdashboard.html", context)
        elif user.role == 'reviewer':
            # Add context data for reviewer dashboard
            context['reviewer_data'] = {}  # Add reviewer-specific data as needed
            return render(request, "reviewerdashboard.html", context)
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

def customerdashboard(request):
    # Your view logic here
    context ={}
    return render(request, 'customerdashboard.html')

def admindashboard(request):
    total_users = CustomUser.objects.count()
    context={'total_users':total_users}
    return render(request, 'admindashboard.html', context)

def reviewerdashboard(request):
    # Your view logic here
    context ={}
    return render(request, 'reviewerdashboard.html')

def vendordashboard(request):
    # Your view logic here
    context ={}
    return render(request, 'vendordashboard.html')

def adduser(request):
    context={}
    return render(request, "adduser.html", context)

# def soft_delete_user(request, user_id):
#     User = get_user_model()
#     user = get_object_or_404(User, pk=user_id)
#     user.is_deleted = True
#     user.save()
#     return JsonResponse({'message': 'User soft deleted successfully'})

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']  # Get the password from the form
            user.set_password(password)  # Set the password using Django's set_password method
            user.save()  # Save the user object to the database
            messages.success(request, 'User added successfully.')
            return redirect('user_list')  
    else:
        form = AddUserForm()
    return render(request, 'adduser.html', {'form': form})

def saveadduser(request):
    m=""
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone_number=request.POST.get('phone_number')
        address=request.POST.get('address')
        role=request.POST.get('role')
        if 'profile_photo' in request.FILES:
            profile_photo = request.FILES['profile_photo']
        else:
            profile_photo = None

        # Create and save the user
        add = CustomUser(username=username, email=email, phone_number=phone_number, address=address, role=role)
        add.set_password(password)  # Set the password
        if profile_photo:
            add.profile_photo = profile_photo  # Assign the profile photo
        add.save()
    
        m="User added successfully!"
    return render(request, 'user_list.html',{'m':m})

def saveupdateuser(request):
    n=""
    if request.method=="POST":
        user_id = request.POST.get('user_id')  # Assuming you have a hidden input field with the user's ID
        user = get_object_or_404(CustomUser, id=user_id)
        user.phone_number=request.POST.get('phone_number')
        user.address=request.POST.get('address')
        if 'profile_photo' in request.FILES:
            profile_photo = request.FILES['profile_photo']
        else:
            profile_photo = None

        # Create and save the user
        # add = CustomUser(phone_number=phone_number, address=address)
        if profile_photo:
            user.profile_photo = profile_photo  # Assign the profile photo
        user.save()
    
        n="User updated successfully!"
    return render(request, 'user_list.html',{'n':n})

def save_update_user(request):
    if request.method == "POST":
        # Fetch the existing user object
        user_id = request.POST.get('user_id')  # Assuming you have a hidden input field with the user's ID
        user = get_object_or_404(CustomUser, id=user_id)
        
        # Update the other details
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        # Add more fields as needed
        
        # Save the updated user object
        user.save()
        messages.success(request, 'User details updated successfully.')
        return redirect('user_list')  # Redirect to the user list page after successful update
    else:
        # Handle GET requests here if needed
        pass

def application(request):
    context={}
    return render(request, "application.html", context)


