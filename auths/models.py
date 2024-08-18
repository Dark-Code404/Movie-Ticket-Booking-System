from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='')
    first_name = models.CharField(max_length=50, blank=True, null=True,default='')
    last_name = models.CharField(max_length=50, blank=True, null=True,default='')
    mobile = models.CharField(max_length=15,default='')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],default='')
    dob = models.CharField(max_length=100,null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,default='')

    def __str__(self):
        return self.user.username
