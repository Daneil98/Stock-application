from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Payment(models.Model):
    user = models.CharField(max_length=200, null = True)
    amount = models.FloatField(default=1000)
    description = models.TextField(max_length=150, blank= True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, null=True)
    
    def __str__(self):
        return f'Deposit {self.amount} - {self.braintree_id}'
    
       
class Buy(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    stock_purchase_price = models.FloatField(null= True)
    total_purchase_amount = models.FloatField(null= True)
    bought = models.BooleanField(default=False)
    shares = models.FloatField(null = True)
    
    def __str__(self):
        return f'Shares {self.shares} - {self.user}'
    
    
class Sell(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    total_selling_amount = models.FloatField(null = True)
    stock_selling_price = models.FloatField(null = True)
    sold = models.BooleanField(default=False)
    shares = models.FloatField(null = True)
    
    
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
    balance = models.FloatField(default=0)
    stock_eq = models.FloatField(default=0)


class Stock_Wallet(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    shares = models.FloatField(null = True) 
    equity = models.FloatField(default=0)
    
    
class Long(models.Model):
    user = models.CharField(max_length=200, null = False)
    name = models.CharField(max_length=200, null=False)
    ticker = models.CharField(max_length=10, null = False)
    amount = models.FloatField(default=0, null = False)
    leverage = models.IntegerField(validators=[MaxValueValidator(10)])
    current_price = models.FloatField(null=True)
    long_price = models.FloatField(null=True)
    returns = models.FloatField(null=True)
    open = models.BooleanField(default=True)
    
    
class Short(models.Model):
    user = models.CharField(max_length=200, null = False)
    name = models.CharField(max_length=200, null=False)
    ticker = models.CharField(max_length=10, null = False)
    amount = models.FloatField(default=0, null = False)
    leverage = models.IntegerField(validators=[MaxValueValidator(10)])
    current_price = models.FloatField(null=True)
    short_price = models.FloatField(null=True)
    returns = models.FloatField(null=True)    
    open = models.BooleanField(default=True)


    
