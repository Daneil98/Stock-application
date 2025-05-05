from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'paid']
    
@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'stock_purchase_price', 'total_purchase_amount', 'shares', 'bought']

@admin.register(amount)
class amountAdmin(admin.ModelAdmin):
    list_display = ['total_price']
    
@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'stock_selling_price', 'total_selling_amount', 'shares', 'sold']


@admin.register(Wallet)
class WallettAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'stock_eq']
    

@admin.register(Stock_Wallet)
class Stock_WallettAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'shares', 'equity']
    
@admin.register(Long)
class LongAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'ticker', 'amount', 'leverage','long_price', 'current_price', 'returns', 'is_open']

@admin.register(Short)
class ShortAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'ticker', 'amount', 'leverage','short_price', 'current_price', 'returns', 'is_open']
