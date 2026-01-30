from django import forms
from django.contrib.auth.models import User
from .models import Payment, Buy, Sell, amount

from django.utils.translation import gettext_lazy as _



#USER ACCOUNT FORMS
    
class BuyForm(forms.ModelForm):
    total_price = forms.FloatField(label='How much do you want to buy?')
    otp = forms.IntegerField(label='Enter code from authenticator:')
    
    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price and total_price <= 0:
            raise forms.ValidationError("Total price must be a positive number.")
        return total_price
    
    class Meta:
        model = amount
        fields = ('total_price', 'otp')      
        
class SellForm(forms.ModelForm):
    total_price = forms.FloatField(label='How much do you want to sell?')
    otp = forms.IntegerField(label='Enter code from authenticator:')
    
    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price and total_price <= 0:
            raise forms.ValidationError("Total price must be a positive number.")
        return total_price
    
    class Meta:
        model = amount
        fields = ('total_price', 'otp')     

class LongForm(forms.ModelForm):
    total_price = forms.FloatField(label='How much do you want to trade?')
    leverage = forms.IntegerField(label='How much leverage do you want (1-10)?')
    otp = forms.IntegerField(label='Enter code from authenticator:')
    
    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price and total_price <= 0:
            raise forms.ValidationError("Total price must be a positive number.")
        return total_price
    
    def clean_leverage(self):
        leverage = self.cleaned_data.get('leverage')
        if leverage and (leverage <= 0 or leverage > 10):
            raise forms.ValidationError("Leverage must be a positive integer between 1 and 10.")
        return leverage
    
    class Meta:
        model = amount
        fields = ('total_price', 'leverage', 'otp')   
        

class ShortForm(forms.ModelForm):
    total_price = forms.FloatField(label='How much do you want to trade?')
    leverage = forms.IntegerField(label='How much leverage do you want (1-10)?')
    otp = forms.IntegerField(label='Enter code from authenticator:')
    
    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price and total_price <= 0:
            raise forms.ValidationError("Total price must be a positive number.")
        return total_price
    
    def clean_leverage(self):
        leverage = self.cleaned_data.get('leverage')
        if leverage and (leverage <= 0 or leverage > 10):
            raise forms.ValidationError("Leverage must be a positive integer between 1 and 10.")
        return leverage
    
    class Meta:
        model = amount
        fields = ('total_price', 'leverage', 'otp')   
        
        
