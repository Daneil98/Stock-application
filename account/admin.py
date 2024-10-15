from django.contrib import admin
from .models import Profile, price_db

# Register your models here.



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

@admin.register(price_db)
class price_dbAdmin(admin.ModelAdmin):
    list_display = ['name', 'closeprice', 'openprice']
