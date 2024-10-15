from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
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
    
    
class amount(models.Model):
    user = models.CharField(max_length=200, blank=True, null=True)
    total_price = models.FloatField(null=True)
    shares = models.FloatField(null=True)
    otp = models.IntegerField(null=True)




class Wallet(models.Model):
    user = models.CharField(max_length=200, null = True)
    balance = models.FloatField(default=0)
    stock_eq = models.FloatField(default=0)

class Stock_Wallet(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    shares = models.FloatField(null = True) 
    equity = models.FloatField(default=0)
    
class Sell(models.Model):
    user = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    total_selling_amount = models.FloatField(null = True)
    stock_selling_price = models.FloatField(null = True)
    sold = models.BooleanField(default=False)
    shares = models.FloatField(null = True)
    
    
    
    def __str__(self):
        return f'Shares {self.shares} - {self.total_selling_amount}'
    
