from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render

# Create your models here.


#USER ACCOUNT MODELS
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'



class Account(models.Model):
      ACCOUNT_TYPES = (
          ('IA' , 'Investment Account' ),
      )
      owner = models.ForeignKey(Profile, on_delete=models.CASCADE, 
      related_name='accounts', verbose_name='The related user')
      account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)
      account_number = models.CharField(max_length=13, unique=True)
      account_balance = models.DecimalField(max_digits=18, decimal_places=2)
      last_deposit = models.DecimalField(max_digits=10, decimal_places=2)
      interest = models.DecimalField(max_digits=3, decimal_places=0)
      date_created = models.DateField(auto_now_add=True)

      def __str__(self):
          return self.account_number



class Transaction(models.Model):
      owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
      from_account = models.CharField(max_length=13)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      date_created = models.DateField(auto_now_add=True)

      def __str__(self):
        return str(self.amount)


