from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Payment, Wallet, Buy, Sell, amount
from .serializers import PaymentSerializer, WalletSerializer, BuySerializer, SellSerializer, AmountSerializer


#PAYMENT VIEWS
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
class PaymentDeposit(APIView):
    def post(self, request, format=None):
        
        
        
        return Response({'Paid': True})


#WALLET VIEWS
class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    
class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
        
        
#BUY VIEWS
class BuyListView(generics.ListAPIView):
    queryset = Buy.objects.all()
    serializer_class = BuySerializer
    
class BuyDetailView(generics.RetrieveAPIView):
    queryset = Buy.objects.all()
    serializer_class = BuySerializer
    
class BuyUpdate(APIView):
    def post(self, request, format=None):
        buy = get_object_or_404(Buy)
        try:
            buy.user.add(request.user)
            buy.name.add(request.name)
            buy.total_purchase_amount.add(request.total_purchase_amount)
            buy.stock_purchase_price.add(request.stock_purchase_price)
            buy.shares.add(request.shares)
            return Response({'bought' : True})   
        except:
            return Response({'sold' : False}) 

#SELL VIEWS
class SellListView(generics.ListAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    
class SellDetailView(generics.RetrieveAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer

class SellUpdate(APIView):
    def post(self, request, format=None):
        sell = get_object_or_404(Sell)
        try:
            sell.user.add(request.user)
            sell.name.add(request.name)
            sell.total_selling_amount.add(request.total_selling_amount)
            sell.stock_selling_price.add(request.stock_selling_price)
            sell.shares.add(request.shares)
            return Response({'sold' : True})   
        except:
            return Response({'sold' : False}) 

#AMOUNT VIEWS
class AmountListView(generics.ListAPIView):
    queryset = amount.objects.all()
    serializer_class = AmountSerializer
    
    
class AmountDetailView(generics.RetrieveAPIView):
    queryset = amount.objects.all()
    serializer_class = AmountSerializer