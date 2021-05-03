from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.

class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_partner = models.BooleanField(default=False)
    
    
class StaffUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    
    
class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    
class Partner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/customer")
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(100,100)],
                                           format='JPEG',
                                           options={'quality':100}
                                           )
    phone = models.CharField(max_length=13)
    
    
    def __str__(self):
        return self.user.username
    
class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13)
    otp = models.IntegerField()
    
    def __str__(self):
        return self.user.username
    
