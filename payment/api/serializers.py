from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Payment, Buy, Sell, amount, Wallet, Stock_Wallet
from account.models import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.ModelSerializer):
    # Include the password explicitly to handle it securely
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User  # This specifies the User model
        fields = ['username', 'password', ]  # Fields you want to serialize

    def create(self, validated_data):
        """
        Override the create method to handle password encryption
        """
        password = validated_data.pop('password')  # Extract the password from the validated data
        user = User(**validated_data)  # Create a User instance without saving it to the database
        user.set_password(password)  # Encrypt the password
        user.save()  # Save the user to the database
        return user
    

class EditSerializer(serializers.Serializer):
    secret = serializers.CharField()    
    
class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payment
        fields = ['amount',]  # Include only relevant fields


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'stock_eq']
        
class StockWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_Wallet
        fields = ['user', 'name', 'equity', 'shares']
        
        
class TickerSerializer(serializers.Serializer):
    ticker = serializers.CharField(label='Ticker', max_length=10)


class BuySerializer(serializers.ModelSerializer):
    
    total_price = serializers.FloatField()
    otp = serializers.IntegerField()
    
    class Meta:
        model = amount
        fields = ['total_price', 'otp']

class SellSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField()
    otp = serializers.IntegerField()
    
    class Meta:
        model = amount
        fields = ['total_price', 'otp']
        
class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = amount
        fields = ['id', 'total_price', 'shares']
        
        
class LongSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField()
    otp = serializers.IntegerField()
    leverage = serializers.IntegerField()
    
    class Meta:
        model = amount
        fields = ['total_price', 'otp', 'leverage']
    
        
class ShortSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
    leverage = serializers.IntegerField()
    otp = serializers.IntegerField()
