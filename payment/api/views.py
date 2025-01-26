from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import *
from ..transaction import *
from account.models import *
from account.tiingo import *
from ..tasks import *
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
import braintree, pyotp

#ACCOUNT API VIEWS

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unrestricted access
    queryset = Profile.objects.all()
    
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the data

        # Save the user (handled by the serializer)
        user = serializer.save()

        # Create a profile for the user
        Profile.objects.create(user=user)

        return Response({'status': 'success', 'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        

class LoginView(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()  
    serializer_class = LoginSerializer


    def post(self, request):
        # Parse the username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate the input data using the serializer
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # This raises errors if data is invalid
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                # Log the user in (creates a session)
                login(request, user)
                return Response({'status': 'success', 'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'message': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)
        else:
            raise AuthenticationFailed("Invalid username or password")



#PAYMENT API VIEWS


class PaymentListView(generics.ListAPIView):
    authentication_classes = [ JWTAuthentication]
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
 

class Dashboard(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = Profile.objects.filter(user=request.user).last()
        wallet = Wallet.objects.filter(user=request.user).last()
        
        if wallet:
            content = {
                'user': user.user.username,
                'balance': wallet.balance, 'stock_eq': wallet.stock_eq    
            }
        
        else:
            content = {
                'user': user.user.username,
                'balance': '0.00',
                'stock_eq': '0.00'    
            }
            
        return Response(content, status=status.HTTP_200_OK) 
    

class Edit(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = Profile.objects.filter(user=request.user).last()
        secret = pyotp.random_base32()
  
        content = {
            'user': user.user.username,
            'secret': secret,   
        }
            
        return Response(content, status=status.HTTP_200_OK) 
    
    def post(self, request):
        user = Profile.objects.filter(user=request.user).last()
        serializer = EditSerializer(data=request.data)
        
        if serializer.is_valid():
            secret = serializer.validated_data['secret']
            user.secret_key = secret
            user.save()
            return Response({'message': 'Secret key successfully updated'}, status=status.HTTP_200_OK) 
        else:
            return Response({'message': 'Secret key successfully updated'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class MyStocks(generics.RetrieveAPIView):
    queryset = Stock_Wallet.objects.all()
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        name = request.user
        
        # Fetch stocks and trades
        stocks_owned = Stock_Wallet.objects.filter(user=name).all()
        long_trades = Long.objects.filter(user=name).all()
        short_trades = Short.objects.filter(user=name).all()

        # Prepare response data
        stocks = []
        for stock in stocks_owned:   
            
            stocks.append({ 
                'stock name': stock.name,
                'equity' : stock.equity,
                'shares' : stock.shares
            })
        
        longs = []  
        for long in long_trades: 
    
            longs.append({ 
                'stock name': long.name,
                'ticker': long.ticker,
                'amount' : long.amount,
                'leverage': long.leverage,
                'execution price' : long.long_price,
                'current price': long.current_price,
                'returns': long.returns,
            })
        
        shorts = [] 
        for short in short_trades: 
             
            shorts.append({ 
                'stock name': short.name,
                'ticker': short.ticker,
                'amount' : short.amount,
                'leverage': short.leverage,
                'execution price' : short.short_price,
                'current price': short.current_price,
                'returns': short.returns,
            })
            
        context = {
            'message': 'Trades and stocks information retrieved successfully.',
            'stocks': stocks,
            'longs': longs,
            'shorts': shorts,
        }

        if not long_trades.exists() and not short_trades.exists() and not stocks_owned.exists():
            context['message'] = 'No trades or stocks available for this user.'

        return Response(context, status=status.HTTP_200_OK)
    

class Ticker(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TickerSerializer(data=request.data)
        user = request.user                             #Request user
        
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']
            prize = {'type': get_price(ticker)}
            price = (prize["type"])                         #Sets price as a dictionary with prize and type as key-value pair
            close_price = price['close']                    # Extracts the "close" value
            open_price = price['open']                      # Extracts the "open" value
            
            name = {'typ': get_meta_data(ticker)}
            meta = (name['typ'])
            stock_name = meta['name']
            
            content = {'stock_name': stock_name, 'meta': meta, 'close_price': close_price, 'open_price': open_price, }
            
            price_db.objects.create(user = user.username, closeprice = close_price, openprice = open_price, name = stock_name, ticker = ticker)
            
            return Response({"content": content}, status=200)
        
        else:
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
class Deposit(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        name = request.user
    
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
        
            try:
                amount = float(amount)
                if amount <= 0:
                    return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
            except (ValueError, TypeError):
                return Response({"error": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

            
            # Create and submit transaction
            try:
                result = gateway.transaction.sale({
                    "amount": str(amount),
                    'payment_method_nonce': 'fake-valid-nonce',
                    "options": {
                        "submit_for_settlement": True,
                    },
                })
            except Exception as e:
                return Response({"error": "Payment gateway error.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if result.is_success:
                self._process_payment(name, amount, result.transaction.id)
                return Response({'status': 'success', 'message': 'Successfully deposited'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Payment failed', 'details': result.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def _process_payment(self, username, amount, transaction_id):
        """Process the wallet and payment updates."""
        # If the user does not have a wallet, create one
        if not Wallet.objects.filter(user=username).exists() and not Payment.objects.filter(user=username).exists():
            Wallet.objects.create(user=username, balance=amount, stock_eq=0.00)
            Payment.objects.create(user=username, amount=amount, paid=True, braintree_id=transaction_id)
        else:
            # Update existing Wallet and Payment records
            wallet_instance = Wallet.objects.filter(user=username).last()
            wallet_instance.balance += amount
            wallet_instance.save()

            payment_instance = Payment.objects.filter(user=username).last()
            payment_instance.amount += amount
            payment_instance.paid = True
            payment_instance.braintree_id = transaction_id
            payment_instance.save()   
        

 
#BUY VIEWS
class StockBuy(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    serializer_class = BuySerializer        
    
    
    def post(self, request, format=None):
        serializer = BuySerializer(data=request.data)
        
        profile = get_object_or_404(Profile, user=request.user)
        name = request.user.username

        
        secret = profile.secret_key
        totp = pyotp.TOTP(secret)
        
        balance = Wallet.objects.filter(user=name).last()       #Balance left in the account
        data = price_db.objects.filter(user=name).last()            #Gets the most recent price entry in the price_db database as a queryset
        prices = float(data.closeprice)                                   #Strips the close-price from the price_db and declares it as a float data type so it can be used in arithmetic operations
        stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
        
        amount1 = float(balance.balance)     #Assigns the wallet balance as a float data type 
        amount3 = float(balance.stock_eq)    #Current stock equity in the wallet assigned
        amount2 = float(prices)             #Current price of the stock to be purchased
        
        if serializer.is_valid():

            sum_price = serializer.validated_data['total_price']
            otp = serializer.validated_data['otp']
            
            #Instance declarations
            WalletTransaction_instance = WalletTransaction(amount1, amount3)
            Transaction_instance = BuyTransaction(amount1)                     #Creates a transaction instance for the transaction class with amount1 as the self.balance
            shares_bought = Transaction_instance.share_number(sum_price, amount2)
            
            
            if Transaction_instance.charge(amount2, shares_bought) and totp.verify(otp):
                    
                if not Stock_Wallet.objects.filter(user=name).exists():
                    shares =  0   
                    stock_equity = 0
                    
                    StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                    Stock_Wallet.objects.create(user = name, name = stock_name,
                        shares = StockHoldingTransaction_instance.buy_shares(shares, shares_bought),            #Calculate the number of shares added and update it 
                        equity = StockHoldingTransaction_instance.buy_stock_eq_update(sum_price)               #Calculate the amount of stock equity added and update it 
                    )
                     
                else:
                    StockWallet_instance = Stock_Wallet.objects.get(name=stock_name)
                    stock_equity = StockWallet_instance.equity
                    StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                    #StockWallet_instance.ticker = ticker
                    StockWallet_instance.user = name
                    StockWallet_instance.name = stock_name
                    shares =  StockWallet_instance.shares               #stocks shares present before current transaction 
                    StockWallet_instance.shares = StockHoldingTransaction_instance.buy_shares(shares, shares_bought)            #Calculate the number of shares added and update it 
                    StockWallet_instance.equity = StockHoldingTransaction_instance.buy_stock_eq_update(sum_price)               #Calculate the amount of stock equity added and update it 
                    StockWallet_instance.save()
                    
                    
                WalletTransaction_instance = WalletTransaction(amount1, amount3)
                Wallet_instance = Wallet.objects.filter(user=name).last()
                Wallet_instance.user = name
                Wallet_instance.balance = WalletTransaction_instance.buy_balance_update(sum_price)      
                Wallet_instance.stock_eq = WalletTransaction_instance.buy_stock_eq_update(sum_price)    
                Wallet_instance.save()
                
                Buy.objects.create(user = name, name = stock_name, bought = True, stock_purchase_price = amount2, total_purchase_amount = sum_price, 
                                   shares = shares_bought)

                data.delete()
                return Response({'status': 'success', 'message': 'Your transaction was successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'message': 'Your transaction was not successful'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class BuyView(generics.RetrieveAPIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    


    def get(self, request):
        stock_buys = Buy.objects.filter(user=request.user.username).all()

        buys = [] 
        for buy in stock_buys: 
             
            buys.append({ 
                'stock name': buy.name,
                'amount' : buy.total_purchase_amount,
                'execution price' : buy.stock_purchase_price,
                'shares': buy.shares,
                'bought': buy.bought,
            })
            
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'buys': buys
        }
        
        return Response(content, status=status.HTTP_200_OK)  
    


#SELL VIEWS   
class StockSell(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    def post(self, request, format=None):
        serializer = SellSerializer(data=request.data)
        name = request.user.username
        profile = get_object_or_404(Profile, user=request.user)
        secret = profile.secret_key
        totp = pyotp.TOTP(secret)
        
        balance = Wallet.objects.filter(user=name).last()       #Balance left in the account
        data = price_db.objects.filter(user=name).last()            #Gets the most recent price entry in the price_db database as a queryset
        stock_price = float(data.openprice)                                   #Strips the close-price from the price_db and declares it as a float data type so it can be used in arithmetic operations
        stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
        
        #BASIC DATA FROM THE WALLET MODEL DB
        balance = Wallet.objects.filter(user=name).last()       #Balance left in the account
        amount1 = wallet_balance = float(balance.balance)      #Assigns the wallet balance as a float data type 
        amount3 = wallet_eq_balance = float(balance.stock_eq)   
        
               
        if serializer.is_valid():
            StockWallet_instance = Stock_Wallet.objects.filter(name=stock_name).last()
    
            if StockWallet_instance is None:
                return Response({'status': 'error', 'message': 'You dont own any shares of this stock'}, status=status.HTTP_400_BAD_REQUEST)

            
            elif stock_name == StockWallet_instance.name:
                
                amount2 = serializer.validated_data['total_price']
                otp = serializer.validated_data['otp']
                Transaction_instance = SellTransaction(amount1)                     #Creates a transaction instance for the transaction class witn amount1 as a data input
                
                WalletTransaction_instance = WalletTransaction(wallet_balance, wallet_eq_balance)
                shares_left = Transaction_instance.share_number(amount2, stock_price)
                
                
                if Transaction_instance.sell(amount2, amount3)and totp.verify(otp):
                    
                    StockWallet_instance = Stock_Wallet.objects.get(name=stock_name)        #Retrieve stock wallet entry/instance by it's stock name
                    stock_equity = StockWallet_instance.equity

                    StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                    StockWallet_instance.user = name
                    StockWallet_instance.name = stock_name
                    StockWallet_instance.shares = StockHoldingTransaction_instance.sell_shares(shares_left, StockWallet_instance.shares)               #Calculate the number of shares sold and update it 
                    StockWallet_instance.equity = StockHoldingTransaction_instance.sell_stock_eq_update(amount2)                        #Calculate the amount of stock equity sold and update it 
                    StockWallet_instance.save()
                        
                    
                    Sell.objects.create(user = name, name = stock_name, sold = True, total_selling_amount = amount2,
                        stock_selling_price = stock_price, shares = shares_left)
                    
                    WalletTransaction_instance = WalletTransaction(amount1, amount3)
                    Wallet_instance = Wallet.objects.filter(user=name).last()
                    Wallet_instance.user = name
                    Wallet_instance.stock_eq = WalletTransaction_instance.sell_stock_eq_update(amount2)
                    Wallet_instance.balance = WalletTransaction_instance.sell_balance_update(amount2)
                    Wallet_instance.save()
                    
                    data.delete()
                    return Response({'status': 'success', 'message': 'Your transaction was successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'failed', 'message': 'Your transaction was not successful'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                            
     
     
        
class SellListView(generics.RetrieveAPIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    


    def get(self, request):
        stock_sells = Sell.objects.filter(user=request.user.username).all()

        sells = [] 
        for sell in stock_sells: 
             
            sells.append({ 
                'stock name': sell.name,
                'amount' : sell.total_selling_amount,
                'execution price' : sell.stock_selling_price,
                'shares': sell.shares,
                'bought': sell.sold,
            })
            
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'sells': sells
        }
        
        return Response(content, status=status.HTTP_200_OK)  


#AMOUNT VIEWS
class AmountView(generics.RetrieveAPIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        amounts = amount.objects.filter(user=request.user.username).all()

        figs = [] 
        for mount in amounts: 
             
            figs.append({ 
                'total amount': mount.total_price,
                'shares' : mount.shares,
                'leverage' : mount.leverage,
                'otp': mount.otp,
            })
            
        content = {
            'user': str(request.user),  # django.contrib.auth.User instance.
            'figs': figs
        }
        
        return Response(content, status=status.HTTP_200_OK)  
    
    
    
    
#TRADING VIEWS
class LongPosition(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = LongSerializer(data=request.data)
        
        profile = get_object_or_404(Profile, user=request.user)
        name = request.user.username
        totp = pyotp.TOTP(profile.secret_key)
        
        # PRICE FETCHING
        balances = Wallet.objects.filter(user=name).last()       #Balance left in the account


        amount1 = float(balances.balance)
        
        data = price_db.objects.filter(user=name).last()            #Gets the most recent price entry in the price_db database as a queryset
        open_price = float(data.openprice)                            #Strips and assings the open price value from price_db as a float data type
        close_price = float(data.closeprice)                          #Strips and assings the close price value from price_db as a float data type
        stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
        ticker = str(data.ticker)

        
        if serializer.is_valid():
            
            sum_price = serializer.validated_data['total_price']
            otp = serializer.validated_data['otp']
            leverage_used = serializer.validated_data['leverage']
            
            #Instance declaration
            Trading_instance = Trading(amount1, leverage_used)                     #Creates a transaction instance for the transaction class with amount1 as the self.balance
            
            
            if totp.verify(otp):
                Long.objects.create(user = name, name = stock_name, ticker = ticker, amount = sum_price, 
                    leverage = leverage_used, current_price = close_price, long_price = open_price, 
                    returns = Trading_instance.long_position(sum_price, open_price, close_price))

               

                balances.balance -= sum_price
                balances.save()
                

                data.delete()
                return Response({'status': 'success', 'message': 'Your transaction was successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'message': 'Your transaction was not successful'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
        

class ShortPosition(APIView):
    authentication_classes = [ JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ShortSerializer
    
    def post(self, request, format=None):
        serializer = ShortSerializer(data=request.data)
        
        #GETS THE USER'S DATA
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        name = user.username
        totp = pyotp.TOTP(profile.secret_key)
        
        # PRICE FETCHING
        balance = Wallet.objects.filter(user=name).last()       #Balance left in the account
        amount1 = float(balance.balance)     #Assigns the wallet balance as a float data type 
                  
        
        data = price_db.objects.filter(user=name).last()            #Gets the most recent price entry in the price_db database as a queryset
        open_price = float(data.openprice)                            #Strips and assings the open price value from price_db as a float data type
        close_price = float(data.closeprice)                          # Current price of the stock
        stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
        ticker = str(data.ticker)      

        
        if serializer.is_valid():
            sum_price = serializer.validated_data['total_price']
            otp = serializer.validated_data['otp']
            leverage_used = serializer.validated_data['leverage']
            
            #Instance declaration
            Trading_instance = Trading(amount1, leverage_used)                     #Creates a transaction instance for the transaction class with amount1 as the self.balance
            
            
            if Trading_instance.short_position(sum_price, open_price, close_price)  and totp.verify(otp):

                Short.objects.create(user = name, name = stock_name, amount = sum_price, ticker = ticker, 
                    leverage = leverage_used, current_price = close_price, short_price = open_price, 
                    returns = Trading_instance.short_position(sum_price, open_price, close_price))
            

                balance.balance -= sum_price
                balance.save()
                
                data.delete()
                return Response({'status': 'success', 'message': 'Your transaction was successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'message': 'Your transaction was not successful'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        