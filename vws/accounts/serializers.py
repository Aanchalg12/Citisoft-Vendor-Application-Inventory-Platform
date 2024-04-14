from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
from .models import UserProfile
from .models import feedback

class ProductSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)  # Add this line

    class Meta:
        model = Product
        fields = ['pk','name', 'website_url', 'vendor_id',  'details', 'pdf_attachment', 'client_id','status','Product_type','tech','tags']
class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('client_id', 'status')  # Only include fields that should be updated
        extra_kwargs = {
            'client_id': {'required': False},
            'status': {'required': False},
        }


    def get_vendor_username(self, obj):
        if obj.vendor_id:
            user = User.objects.filter(id=obj.vendor_id).first()
            if user:
                return user.username
        return None  
    

class UserProfileSerializers(serializers.ModelSerializer):
        class Meta:
            model = UserProfile
            fields = '__all__' 


class UserProfileSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source='userprofile.role_id')
    emp_id = serializers.IntegerField(source='userprofile.emp_id')
    number = serializers.IntegerField(source='userprofile.number')


    class Meta:
        model = User
        fields = '__all__' 

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = feedback
        fields = ['product_id', 'status', 'sent_id', 'rec_id', 'text']
