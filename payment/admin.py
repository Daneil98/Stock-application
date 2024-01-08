from django.contrib import admin
from .models import Payment, Buy, amount
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'paid']
    
@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'stock_purchase_price','total_purchase_price', 'shares', 'bought', 'balance']

@admin.register(amount)
class amountAdmin(admin.ModelAdmin):
    list_display = ['total_purchase_price']