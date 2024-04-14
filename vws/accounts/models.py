from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_id = models.IntegerField(choices=((0, 'Admin'), (1, 'Vendor'), (2, 'Client')))
    emp_id = models.IntegerField(null=True, blank=True)
    number=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_id_display()}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    website_url = models.URLField(max_length=1024, blank=True, null=True)
    vendor_id = models.IntegerField(null=True, blank=True)
    details = models.TextField()
    pdf_attachment = models.FileField(upload_to='product_pdfs/', blank=True, null=True)
    client_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(default=0)
    tags = models.CharField(max_length=255, blank=True, help_text="Enter tags separated by commas.")
    Product_type = models.CharField(max_length=255, blank=True, help_text="Enter type separated by commas.")
    tech = models.CharField(max_length=255, blank=True, help_text="Enter type tech by commas.")

class suggestion(models.Model):
    
    product_id = models.IntegerField()
    status = models.IntegerField(default=0)
    client_id = models.IntegerField(null=True, blank=True)
    vendor_id = models.IntegerField(null=True, blank=True)
    suggestion_details = models.CharField(max_length=255, blank=True)


class feedback(models.Model):
    
    product_id = models.IntegerField()
    status = models.IntegerField(default=0)
    sent_id = models.IntegerField(null=True, blank=True)
    rec_id = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

