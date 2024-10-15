from django import forms
from django.contrib.auth.models import User
from .models import Payment, Buy, Sell, amount
from socket import fromshare
from django.utils.translation import gettext_lazy as _



#USER ACCOUNT FORMS

class WithdrawForm(forms.ModelForm):
    amount = forms.FloatField(label='How much do you want to deposit?')
    description = forms.CharField(label='add a note to your payment', required=False)
    
    class Meta:
        model = Payment
        fields = ('amount', 'description')

class BuyForm(forms.ModelForm):
    total_price = forms.FloatField(label='How much do you want to buy?')
    otp = forms.IntegerField(label='Enter code from authenticator:')
    
    class Meta:
        model = amount
        fields = ('total_price', 'otp')      
        
class SellForm(forms.ModelForm):
    total_price = forms.FloatField(label='How much do you want to sell?')
    otp = forms.IntegerField(label='Enter code from authenticator:')
    
    class Meta:
        model = amount
        fields = ('total_price', 'otp')     
