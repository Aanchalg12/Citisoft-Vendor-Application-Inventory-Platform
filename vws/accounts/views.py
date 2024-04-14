from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Product
from django.contrib.auth.hashers import make_password
from .models import UserProfile
import json
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from django.http import FileResponse, Http404
from django.conf import settings
import os
from .serializers import UserProfileSerializer
from .serializers import ProductUpdateSerializer
from .serializers import FeedbackSerializer

from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import feedback



@api_view(['GET'])
def user_list(request):
    """
    List all users or filter them by 'role_id'.
    """
    # Start with all users, prefetching profiles to minimize database queries
    queryset = User.objects.all().select_related('userprofile')
    
    # Check for 'role_id' in query parameters and filter if present
    role_id = request.query_params.get('role_id')
    print(role_id)
    if role_id is not None:
        queryset = queryset.filter(userprofile__role_id=role_id)
    
    # Serialize the queryset
    serializer = UserProfileSerializer(queryset, many=True)
    
    # Return the serialized data
    return Response(serializer.data)

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserProfileSerializers


@api_view(['GET'])
def get_all_user_profiles(request):
    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializers(profiles, many=True)
        return Response(serializer.data)


@api_view(['PUT'])
def update_product(request, product_id):
    """
    Update a product instance.
    """
    product = get_object_or_404(Product, pk=product_id)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_product_info(request, product_id):
    """
    Update the 'client_id' and optionally 'status' of a Product.
    """
    product = get_object_or_404(Product, pk=product_id)
    serializer = ProductUpdateSerializer(product, data=request.data, partial=True)  # Allow partial updates
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'vendor_id', 'client_id']

@api_view(['GET'])
def product_list(request):
    # Start with all products
    queryset = Product.objects.all()
    
    # Apply filters
    my_filter = ProductFilter(request.GET, queryset=queryset)
    filtered_qs = my_filter.qs
    
    # Serialize the filtered queryset
    serializer = ProductSerializer(filtered_qs, many=True)
    return Response(serializer.data)

def download_docx(request, filename):
    print(filename)
    file_path = os.path.join(settings.MEDIA_ROOT, 'product_pdfs', filename)
    
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, filename=filename)
    else:
        raise Http404("The requested docx file does not exist.")


def login_view(request):
    return render(request, 'accounts/login.html')

def signup_view(request):
    return render(request, 'accounts/signup.html')

def vendor_home_view(request):
    return render(request, 'accounts/vendor_home.html')

def listselectproducts_view(request):
    return render(request, 'accounts/select_products.html')
def listclients(request):
    return render(request, 'accounts/listclients.html')
def viewproductvendor(request):
    return render(request, 'accounts/viewvendorproduct.html')
def viewvendorprofile(request):
    return render(request, 'accounts/vendor_profile.html')
def listvendors_view(request):
    return render(request, 'accounts/listvendors.html')
def clienthome_view(request):
    return render(request, 'accounts/client_home.html')
def create_product_view(request):
    return render(request, 'accounts/create_product.html')
def viewproduct_view(request):
     return render(request, 'accounts/viewproduct.html')
def listinterseted_view(request):
     return render(request, 'accounts/interseted.html')
def profile_view(request):
     return render(request, 'accounts/myprofile.html')
def view_client(request):
     return render(request, 'accounts/viewclient.html')
def vendore_myprofile(request):
     return render(request, 'accounts/vendore_myprofile.html')
      
def get_feedback_messages(request):
    # Get product_id from the request query parameters
    product_id = request.GET.get('product_id')

    # Initialize the queryset for messages
    if product_id:
        # If product_id is provided, filter messages by product_id
        messages = feedback.objects.filter(product_id=product_id).values(
            'id', 'product_id', 'text', 'sent_id', 'rec_id', 'status'
        )
    else:
        # If no product_id is provided, retrieve all messages
        messages = feedback.objects.all().values(
            'id', 'product_id', 'text', 'sent_id', 'rec_id', 'status'
        )

    # Return the messages as JSON
    return JsonResponse(list(messages), safe=False)



@api_view(['POST'])
def craeteProduct_api(request):
    # user = request.user
    # if not user.is_authenticated:
    #     return Response({"message": "User not authenticated"}, status=403)
    serializer = ProductSerializer(data=request.data);

    if serializer.is_valid():
        product = serializer.save()
        # You can include additional product details in the response as needed
        response_data = {
            "message": "Product created successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                # Include other fields as needed
            }
        }
        return Response(response_data, status=201)
    else:
        return Response(serializer.errors, status=400)



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # Parsing JSON data
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id')

        if not (username and email and password and role_id is not None):
            return JsonResponse({'error': 'Missing data'}, status=400)

        # Creating the User instance
        user = User.objects.create(username=username, email=email)
        user.password = make_password(password)
        user.save()

        # Creating the UserProfile instance with role_id
        UserProfile.objects.create(user=user, role_id=role_id)

        return JsonResponse({'success': 'User created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
