from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

# Create your models here.


#USER ACCOUNT MODEL
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=255, null= True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'


class price_db(models.Model):
    user = models.CharField(max_length=200, null = True)
    ticker = models.CharField(max_length=20, null = False)
    name = models.CharField(max_length=100, null=True) 
    closeprice = models.CharField(max_length=10, null=True)   
    openprice = models.CharField(max_length=10, null=True)  

    @cached_property
    def data(self):
    # Expensive operation e.g. external service call
        return "{0} {1} {2} {3} {4}".format(self.user, self.ticker, self.name, self.closeprice, self.openprice)

class FinancialData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    news_text = models.TextField(null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'date']),
        ]
        