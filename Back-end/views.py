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
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import ApplicationForm
from .models import Application
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .forms import VendorDetailsForm
from .models import Vendor_Info



def user_list(request):
    # Query all non-deleted users
    users = CustomUser.objects.filter(is_deleted=False)

    # Paginate each queryset
    vendors = CustomUser.objects.filter(role='vendor', is_deleted=False).order_by('id').values('username', 'email', 'phone_number', 'address', 'id')
    customers = CustomUser.objects.filter(role='customer', is_deleted=False).order_by('id').values('username', 'email', 'phone_number', 'address', 'id')
    reviewers = CustomUser.objects.filter(role='reviewer', is_deleted=False).order_by('id').values('username', 'email', 'phone_number', 'address', 'id')

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

    return render(request, 'user_list.html', {
        'vendor_page_obj': vendor_page_obj,
        'customer_page_obj': customer_page_obj,
        'reviewer_page_obj': reviewer_page_obj,
        'users': users,
    })

# @permission_required('myCitisoft.can_delete_user')
def deleteuser(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == 'POST':
        user.delete()
        # messages.success(request, "User is deleted")
        return redirect('user_list')  # Redirect to a success page
    else:
        # Render the delete user confirmation page
        return render(request, 'deleteuser.html', {'user': user})

def home(request):
    return render(request, 'home.html')

class UserListView(ListView):
    paginate_by = 4  # Number of users per page
    template_name = 'user_list.html'  # Your template name
    context_object_name = 'user_list'  # Name of the context variable in the template

    def get_queryset(self):
        # Query all non-deleted users
        return CustomUser.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['user_list']
        paginator = Paginator(users, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

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

def addapplication(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application')  # Redirect to home page after successful submission
    else:
        form = ApplicationForm()
    return render(request, 'addapplication.html', {'form': form})
    


# def search_users(request):
#     query = request.GET.get('query')
#     if query:
#         users = CustomUser.objects.filter(username__icontains=query)
#     else:
#         users = None

#     return render(request, 'search_results.html', {'users': users, 'query': query})

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
    total_applications = Application.objects.count()
    context = {
        'total_users': total_users,
        'total_applications': total_applications,
    }
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
    applications = Application.objects.all()
    return render(request, 'application.html', {'applications': applications})
 
def application_details(request, pk):
    application = get_object_or_404(Application, pk=pk, is_deleted=False)
    return render(request, 'application_details.html', {'application': application})

def update_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_details', pk=pk)
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'update_application.html', {'form': form, 'application': application})

def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        return redirect('application')  
    else:
        return render(request, 'delete_application.html', {'application': application})
    
# def search_application(request):
#     query = request.GET.get('query')
#     if query:
#         applications = Application.objects.filter(name__icontains=query, is_deleted=False)
#     else:
#         applications = Application.objects.filter(is_deleted=False)
#     return render(request, 'search_application.html', {'applications': applications, 'query': query})
# def search_users(request):
#     query = request.GET.get('query')
#     if query:
#         users = CustomUser.objects.filter(username__icontains=query)
#     else:
#         users = None

#     return render(request, 'search_results.html', {'users': users, 'query': query})

def search_results(request):
    query = request.GET.get('query')
    search_type = request.GET.get('search_type')
    results = []

    if search_type == 'user':
        if query:
            results = CustomUser.objects.filter(username__icontains=query)
    elif search_type == 'application':
        if query:
            results = Application.objects.filter(title__icontains=query)
    elif search_type == 'vendor':
        if query:
            results = Vendor_Info.objects.filter(vendor_name__icontains=query)
    

    return render(request, 'search_results.html', {'results': results, 'query': query})

def generate_report(request, application_id):
    # Get the specific application from the database
    try:
        application = Application.objects.get(pk=application_id, is_deleted=False)
    except Application.DoesNotExist:
        return HttpResponse("Application not found.", status=404)

    # Create a BytesIO buffer to hold the PDF content
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Define styles for the document
    styles = getSampleStyleSheet()

    # Add application picture to the document
    if application.picture:
        picture = Image(application.picture.path, width=200, height=200)
        elements.append(picture)
        elements.append(Spacer(1, 20))

    # Add application details to the document
    elements.append(Paragraph(f"<b>Application Title:</b> {application.title}", styles['Normal']))
    elements.append(Paragraph(f"<b>Description:</b> {application.description}", styles['Normal']))
    elements.append(Paragraph(f"<b>Vendor Name:</b> {application.vendor_name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Software Type:</b> {application.software_type}", styles['Normal']))
    elements.append(Paragraph(f"<b>Additional Information:</b> {application.additional_information}", styles['Normal']))
    elements.append(Paragraph(f"<b>Comments:</b> {application.comments}", styles['Normal']))
    elements.append(Paragraph(f"<b>Ratings:</b> {application.ratings}", styles['Normal']))
    elements.append(Paragraph(f"<b>Vendor Company URL:</b> {application.vendor_company_link}", styles['Normal']))
    elements.append(Paragraph(f"<b>Contact Vendor:</b> {application.contact_vendor}", styles['Normal']))

    # Build PDF document
    doc.build(elements)

    # Get PDF content from BytesIO buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    # Create an HttpResponse object with PDF content
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="application_report.pdf"'
    return response

def vendor_details(request):
    vendors = Vendor_Info.objects.all()
    return render(request, 'vendor_details.html', {'vendors': vendors})

def vendor_details_add(request):
    # if request.method == 'POST':
    #     form = VendorDetailsForm(request.POST)
    #     if form.is_valid():
    #         print(request.POST)
    #         form.save()
    #         return redirect('vendor_details') 
    if request.method == 'POST':
        print("Form submitted")
        form = VendorDetailsForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            print("Data saved to database")
            return redirect('vendor_details')
    else:
        print(form.errors)
        form = VendorDetailsForm()
    return render(request, 'vendor_details_add.html', {'form': form})

def vendor_details_add(request):
    if request.method == 'POST':
        form = VendorDetailsForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('vendor_details')
        except Exception as e:
            print(e)
            return render(request, 'vendor_details.html', {'error_message': str(e)})
    else:
        form = VendorDetailsForm()
    return render(request, 'vendor_details_add.html', {'form': form})

def update_vendor_info(request, vendor_info_id):
    vendor_info = get_object_or_404(Vendor_Info, pk=vendor_info_id)
    if request.method == 'POST':
        form = VendorDetailsForm(request.POST, instance=vendor_info)
        if form.is_valid():
            form.save()
            return redirect('vendor_details')  # Redirect to the details page or any other page
    else:
        form = VendorDetailsForm(instance=vendor_info)
    context = {
        'form': form,
        'vendor_info_id': vendor_info_id,
    }
    return render(request, 'update_vendor_info.html', context)


def vendor_detail_info(request, vendor_id):
    vendor = Vendor_Info.objects.get(pk=vendor_id)
    context = {'vendor': vendor}
    return render(request, 'vendor_detail_info.html', context)

def delete_vendor_info(request, vendor_info_id):
    vendor_info = get_object_or_404(Vendor_Info, pk=vendor_info_id)
    
    if request.method == 'POST':
        vendor_info.delete()
        return redirect('vendor_details')  # Redirect to the details page or any other page
    else:
        return render(request, 'delete_vendor_info.html', {'vendor_info': vendor_info})

def generate_vendor_info_pdf(response, vendor_info_id): 
    vendor = get_object_or_404(Vendor_Info, pk=vendor_info_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="vendor_info_report.pdf"'
    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    bold_style = ParagraphStyle(name='Bold', parent=normal_style, fontName='Helvetica-Bold')
    # Create content
    content = []
    # Add title
    content.append(Paragraph('Vendor Information Report', title_style))
    content.append(Spacer(1, 12))
    # Add vendor details
    content.append(Paragraph('Vendor Name: {}'.format(vendor.vendor_name), bold_style))
    content.append(Paragraph('Phone Number: {}'.format(vendor.phone_number), normal_style))
    content.append(Paragraph('Address: {}'.format(vendor.address), normal_style))
    content.append(Paragraph('Established Date: {}'.format(vendor.established_year), normal_style))
    content.append(Paragraph('Number of Employees: {}'.format(vendor.number_of_employees), normal_style))
    content.append(Paragraph('Location Countries: {}'.format(vendor.location_countries), normal_style))
    content.append(Paragraph('Location Cities: {}'.format(vendor.location_cities), normal_style))
    content.append(Paragraph('Business Area: {}'.format(vendor.business_area), normal_style))
    content.append(Paragraph('Financial Services Client Types: {}'.format(vendor.financial_services_client_types), normal_style))
    content.append(Paragraph('Company URL: {}'.format(vendor.vendor_company_link), normal_style))
    content.append(Paragraph('Internal Professional Services: {}'.format(vendor.internal_professional_services), normal_style))
    # Build PDF document
    doc.build(content)
    return response
