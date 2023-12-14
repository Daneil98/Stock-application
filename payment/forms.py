from django import forms
from django.contrib.auth.models import User
from .models import Payment
from socket import fromshare
from django.utils.translation import gettext_lazy as _



#USER ACCOUNT FORMS

class DepositForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='How much do you want to deposit?')
    description = forms.CharField(label='add a note to your payment', required=False)
    
    class Meta:
        model = Payment
        fields = ('amount', 'description')


        