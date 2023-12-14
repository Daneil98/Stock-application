from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    description = models.TextField(max_length=150, blank= True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, null=True)
    
    def __str__(self):
        return f'Deposit {self.amount} - {self.id}'
    
 
    
    
