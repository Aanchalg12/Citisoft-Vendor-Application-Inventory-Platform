from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
        ('reviewer', 'Reviewer'),
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=ROLES, default='customer') 
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def undelete(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_delete_user", "Can delete user"),
            ("view_all_users", "Can view all users"),
            ("edit_all_users", "Can edit all users"),
            ("can_add_user", "Can add user"),
        ]

class Application(models.Model):
    CLOUD_CHOICES = [
        ('Enabled', 'Enabled'),
        ('Native', 'Native'),
        ('Based', 'Based'),
    ]

    STATUS = [
         ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    ]
    picture = models.ImageField(upload_to='application_pictures/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    vendor_name = models.CharField(max_length=100)
    software_type = models.CharField(max_length=50)
    additional_information = models.TextField()
    comments = models.TextField()
    ratings = models.DecimalField(max_digits=5, decimal_places=2)
    vendor_company_link = models.URLField()
    contact_vendor = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null = True, choices=STATUS)
    cloud = models.CharField(max_length=10, choices=CLOUD_CHOICES, default='Enabled')
    last_demo_date = models.DateField(null=True, blank=True)
    last_reviewed_date = models.DateField(null=True, blank=True)
    modules = models.CharField(max_length=50, default='NA')

    class Meta:
        permissions = [
            ("can_delete_application", "Can delete application"),
            ("view_all_applications", "Can view all applications"),
            ("edit_all_applications", "Can edit all applications"),
            ("can_add_application", "Can add application"),
        ]


class Vendor_Info(models.Model):
    SERVICES = [
         ('Yes', 'Yes'),
         ('No', 'No'),
    ]

    vendor_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    established_year = models.DateField()
    number_of_employees = models.PositiveIntegerField()
    location_countries = models.CharField(max_length=50)
    location_cities = models.CharField(max_length=50)
    business_area = models.CharField(max_length=100)
    financial_services_client_types = models.TextField()
    vendor_company_link = models.URLField()
    internal_professional_services = models.CharField(max_length=20, null = True, choices=SERVICES)

    class Meta:
        permissions = [
            ("can_delete_vendor_info", "Can delete vendor_info"),
            ("view_all_vendor_info", "Can view all vendor_info"),
            ("edit_all_vendor_info", "Can edit all vendor_info"),
            ("can_add_vendor_info", "Can add vendor_info"),
        ]

