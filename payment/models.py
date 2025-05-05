from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from .cache_utils import *

# Create your models here.

class Payment(models.Model):
    user = models.CharField(max_length=200, null = True)
    amount =models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    description = models.TextField(max_length=150, blank= True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, null=True)
    
    def __str__(self):
        return f'Deposit {self.amount} - {self.braintree_id}'
    
       
class Buy(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    stock_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bought = models.BooleanField(default=False)
    shares = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    def __str__(self):
        return f'Shares {self.shares} - {self.user}'
    
    
class Sell(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    total_selling_amount = models.FloatField(null = True)
    stock_selling_price = models.FloatField(null = True)
    sold = models.BooleanField(default=False)
    shares = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    
    def __str__(self):
        return f'Shares {self.shares} - {self.total_selling_amount}'
    
    
class amount(models.Model):
    user = models.CharField(max_length=200, blank=True, null=True)
    total_price = models.FloatField(null=True)
    shares = models.FloatField(null=True)
    leverage = models.IntegerField(validators=[MaxValueValidator(10)], null=True, default=1)
    otp = models.IntegerField(null=True)

    def clean(self):
        super().clean()
        if self.leverage > 10:
            raise ValidationError({'leverage': 'leverage cannot exceed 10x'})


class Wallet(models.Model):
    user = models.CharField(max_length=200, null = True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_eq = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @classmethod
    def get_for_user(cls, user_id):
        return get_cached_wallet(user_id)


class Stock_Wallet(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    shares = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    equity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    
class Long(models.Model):
    user = models.CharField(max_length=200, null = False)
    name = models.CharField(max_length=200, null=False)
    ticker = models.CharField(max_length=10, null = False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    leverage = models.IntegerField(validators=[MaxValueValidator(10)])
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    long_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    returns = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_open = models.BooleanField(default=True)
    
    @classmethod
    def close(self):
        self.is_open = False
        self.save()
    
    
class Short(models.Model):
    user = models.CharField(max_length=200, null = False)
    name = models.CharField(max_length=200, null=False)
    ticker = models.CharField(max_length=10, null = False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    leverage = models.IntegerField(validators=[MaxValueValidator(10)])
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    short_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    returns = models.DecimalField(max_digits=10, decimal_places=2, null=True)    
    is_open = models.BooleanField(default=True)

    @classmethod    
    def close(self):
        self.is_open = False
        self.save()


    
