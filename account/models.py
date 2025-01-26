from django.db import models
from django.conf import settings

# Create your models here.


#USER ACCOUNT MODEL
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=255, null= True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'


class price_db(models.Model):
    user = models.CharField(max_length=200, null = True)
    ticker = models.CharField(max_length=10, null = False)
    name = models.CharField(max_length=10, null=True) 
    closeprice = models.CharField(max_length=10, null=True)   
    openprice = models.CharField(max_length=10, null=True)  
