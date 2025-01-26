from django import forms
from django.contrib.auth.models import User
from .models import Profile, price_db
from socket import fromshare
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _



#USER ACCOUNT FORMS
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'secret_key',)

class FAQForm(forms.Form):
    question = forms.CharField(label='Question', max_length=150, required=False)




#STOCK FORMS
class TickerForm(forms.Form):
    ticker = forms.CharField(label='Ticker', max_length=10)
    

