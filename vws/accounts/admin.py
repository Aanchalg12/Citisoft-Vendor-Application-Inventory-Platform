from django.contrib import admin
from .models import UserProfile
from .models import Product

admin.site.register(UserProfile)
admin.site.register(Product)
