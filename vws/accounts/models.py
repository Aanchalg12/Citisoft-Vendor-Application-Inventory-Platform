from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_id = models.IntegerField(choices=((0, 'Admin'), (1, 'Vendor'), (2, 'Client')))
    emp_id = models.IntegerField(null=True, blank=True)
    number=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_id_display()}"


class feedback(models.Model):
    
    product_id = models.IntegerField()
    status = models.IntegerField(default=0)
    sent_id = models.IntegerField(null=True, blank=True)
    rec_id = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

