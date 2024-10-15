from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from ..models import Payment, Wallet, Buy, Sell, amount, Stock_Wallet
from .serializers import PaymentSerializer, WalletSerializer, BuySerializer, SellSerializer, AmountSerializer, StockWalletSerializer


#PAYMENT VIEWS
class PaymentListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'Deposits': serializer.data
        }
        
        return Response(content)
    
class Payment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    queryset = Payment.objects.all()  
    serializer_class = BuySerializer

    def post(self, request, format=None):
        pay = Payment()  # Create a new Buy object
        serializer = PaymentSerializer(pay, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'created', 'pay': serializer.data})
        else:
            return Response({'status': 'failed', 'errors': serializer.errors})


#WALLET VIEWS
class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'Wallet List': serializer.data
        }
        
        return Response(content)  
    
class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'Wallet Details': serializer.data
        }
        
        return Response(content)     
    
#STOCK WALLET VIEWS
class StockWalletView(generics.RetrieveAPIView):    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Stock_Wallet.objects.all()
    serializer_class = StockWalletSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'stocks': serializer.data
        }
        
        return Response(content)  
    
class StockWalletUpdate(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    queryset = Stock_Wallet.objects.all()  
    serializer_class = StockWalletSerializer


    def post(self, request, format=None):
        name = request.data.get('name')
        try:
            SW = Stock_Wallet.objects.get(name=name)
        except Stock_Wallet.DoesNotExist:
            SW = Stock_Wallet()  # Create a new Stock_Wallet object
        serializer = StockWalletSerializer(SW, data=request.data)
        if serializer.is_valid():
            serializer.save(user=SW.user)
            return Response({'status': 'created', 'SW': serializer.data})
        else:
            return Response({'status': 'failed', 'errors': serializer.errors})
    
    
#BUY VIEWS
class BuyView(generics.ListAPIView):
    queryset = Buy.objects.all()
    serializer_class = BuySerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'Shares purchased': serializer.data
        }
        
        return Response(content)  
    
class BuyUpdate(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    queryset = Buy.objects.all()  
    serializer_class = BuySerializer

    def post(self, request, format=None):
        buy = Buy()  # Create a new Buy object
        serializer = BuySerializer(buy, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'created', 'buy': serializer.data})
        else:
            return Response({'status': 'failed', 'errors': serializer.errors})

#SELL VIEWS   
class SellDetailView(generics.RetrieveAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'Sold Stocks': serializer.data
        }
        
        return Response(content)  

class SellUpdate(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    queryset = Sell.objects.all()  
    serializer_class = SellSerializer
    
    def post(self, request, format=None):
        sell = Sell()
        serializer = SellSerializer(sell, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'created', 'sell': serializer.data})   
        else:
            return Response({'status': 'failed', 'errors': serializer.errors}) 


#AMOUNT VIEWS
class AmountView(generics.RetrieveAPIView):
    queryset = amount.objects.all()
    serializer_class = AmountSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
            'price data': serializer.data
        }
        
        return Response(content)  