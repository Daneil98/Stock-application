from rest_framework import serializers
from ..models import Payment, Buy, Sell, amount, Wallet, Stock_Wallet


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'description', 'paid', 'braintree_id']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'stock_eq']
        
class StockWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_Wallet
        fields = ['user', 'name', 'equity', 'shares']


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'

class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = ['id', 'user', 'name', 'stock_selling_price', 'total_selling_amount', 'sold', 'shares']
        
class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = amount
        fields = ['id', 'total_price', 'shares']