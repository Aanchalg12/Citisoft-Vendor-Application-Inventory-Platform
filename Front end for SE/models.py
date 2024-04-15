from django.db import models

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    website = models.URLField()
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/')
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.vendor_name + ' - ' + self.product_name
