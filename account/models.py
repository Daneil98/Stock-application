from django.db import models
from django.conf import settings

# Create your models here.


#USER ACCOUNT MODEL
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    address = models.CharField(max_length=120, blank=True)
    secret_key = models.CharField(max_length=255, null= True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'


class price_db(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=10, null=True) 
    closeprice = models.CharField(max_length=10, null=True)   
    openprice = models.CharField(max_length=10, null=True)  
