import braintree
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import *
from .models import *
from .tasks import *
from account.models import Profile, price_db
from django.urls import reverse
from payment.transaction import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pyotp
from django.http import JsonResponse


# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


#DEPOSIT VIEWS
@login_required
def payment_process(request):
    
    Payment_id = request.session.get('Payment_id')
    user_name = request.user.username
    
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        
        amount = request.POST.get("amount")
        
        if amount:  # Check if the value exists
            amount = float(amount)
            try:
                if amount > 0:  # Validate that the amount is positive
                    # create and submit transaction
                    result = gateway.transaction.sale({
                        "amount": str(amount),
                        'payment_method_nonce': 'fake-valid-nonce',
                        "options" : {
                            "submit_for_settlement": True, # Required
                        },  
                    })
                else:
                    return JsonResponse({"error": "Amount must be greater than zero."}, status=400)
            except ValueError:
                # Handle case where the amount is not a valid float
                return JsonResponse({"error": "Invalid amount format."}, status=400)
        else:
            # Handle case where the amount is not provided
            return JsonResponse({"error": "Amount not provided."}, status=400)


        # create and submit transaction
        if result and result.is_success:

            if not Wallet.objects.filter(user=user_name).exists() and not Payment.objects.filter(user=user_name).exists():
                Wallet.objects.create(user = user_name, balance = amount, stock_eq = 0.00)
                Payment.objects.create(user = user_name, amount = amount, paid = True, braintree_id = result.transaction.id)
            
            else:    
                Payment_instance = Payment.objects.filter(user=user_name).last()
                Payment_instance.user = user_name
                Payment_instance.amount += amount
                # mark the order as paid
                Payment_instance.paid = True
                # store the unique transaction id
                Payment_instance.braintree_id = result.transaction.id
                
                
                Wallet_instance = Wallet.objects.filter(user=user_name).last()
                Wallet_instance.balance += amount
                Wallet_instance.user = user_name
                
                # save the payment
                Payment_instance.save()
                Wallet_instance.save()
                   
            
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
    # generate token
        client_token = 'sandbox_rz4k7rvw_qnk7x4t299nm2wdy'
        return render(request, 'process.html', {'Payment': Payment, 'client_token': client_token})


@login_required
def payment_done(request):
    return render(request, 'payment/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')



#STOCK BUY & SELL VIEWS
@login_required
def stock_buy(request):
    form = BuyForm(request.POST)
#    sign = True                                     # Helps determine what kind of operation is ongoing
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    # PRICE FETCHING
    balance = Wallet.objects.filter(user=name).last()       #Balance left in the account
    data = price_db.objects.filter(user=name).last()            #Gets the most recent price entry in the price_db database as a queryset

    
    #DATA EXTRACTION
    prices = float(data.closeprice)                                   #Strips the close-price from the price_db and declares it as a float data type so it can be used in arithmetic operations
    stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
#   ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    wallet_balance = float(balance.balance)                        #Assigns the wallet balance as a float data type 
    stock_eq = float(balance.stock_eq)                       #Current stock equity in the wallet assigned

    amount1 = float(balance.balance)     #Assigns the wallet balance as a float data type 
    amount3 = float(balance.stock_eq)    #Current stock equity in the wallet assigned
    amount2 = float(prices)             #Current price of the stock to be purchased
    
    if request.method == "POST":
        if form.is_valid():
            total_amount = form.save(commit=False)
            total_amount.user = name
            total_amount.save()
            
            sum_price = float(total_amount.total_price)
            otp = total_amount.otp
            shares_bought = float(sum_price / prices)
            
            if totp.verify(otp):
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
                    StockWallet_instance.save(commit=False)
                    
                    
                WalletTransaction_instance = WalletTransaction(amount1, amount3)
                Wallet_instance = Wallet.objects.filter(user=name).last()
                Wallet_instance.user = name
                Wallet_instance.balance = WalletTransaction_instance.buy_balance_update(sum_price)      
                Wallet_instance.stock_eq = WalletTransaction_instance.buy_stock_eq_update(sum_price)    
                Wallet_instance.save(commit=False)
                
                Buy.objects.create(user = name, name = stock_name, bought = True, stock_purchase_price = amount2, total_purchase_amount = sum_price, 
                                   shares = shares_bought)            
                
                StockWallet_instance.save()
                Wallet_instance.save()
                total_amount.delete()                                                               #Deletes amount_db entry
                data.delete()                                                                       #Deletes price_db entry
                
                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
    
    return render(request, 'stock_buy.html', {'Buy': Buy, 'form': form, 'total': wallet_balance, 'prices': prices, 'stock': stock_name })
    
    
            
@login_required        
def stock_sell(request):
    form = SellForm(request.POST)
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    name = user_name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    #PRICE FETCHING
    data = price_db.objects.filter(user=user_name).last()                #Gets the most recent price entry in the price_db database as a queryset
    balance = Wallet.objects.filter(user=user_name).last()             #Balance left in the account
    
    #DATA EXTRACTION
    stock_price = float(data.openprice)                             #Strips and assings the open price value from price_db as a float data type
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
#   ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    amount1 = wallet_balance = float(balance.balance)      #Assigns the wallet balance as a float data type 
    amount3 = wallet_eq_balance = float(balance.stock_eq)         
    
    
    #STOCK DATA FROM THE BUY MODEL DB
    StockWallet_instance = Stock_Wallet.objects.filter(user=user_name, name=stock_name).last()

    if StockWallet_instance is None:
        return redirect('my_stocks')

    if request.method == "POST":
        if stock_name == StockWallet_instance.name:
            if form.is_valid():
                data2 = form.save(commit=False)
                data2.user = user_name
                data2.save()

                amount2 = float(data2.total_price)                                          # Equity user wants to sell
                otp = data2.otp                                                               # otp code
                
                shares_left = float(amount2/stock_price)                                    #Calculates the number of shares to be sold
                
                if totp.verify(otp):
                    StockWallet_instance = Stock_Wallet.objects.get(name=stock_name)        #Retrieve stock wallet entry/instance by it's stock name
                    stock_equity = StockWallet_instance.equity

                    StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                    StockWallet_instance.user = name
                    StockWallet_instance.name = stock_name
                    StockWallet_instance.shares = StockHoldingTransaction_instance.sell_shares(shares_left, StockWallet_instance.shares)               #Calculate the number of shares sold and update it 
                    StockWallet_instance.equity = StockHoldingTransaction_instance.sell_stock_eq_update(amount2)                        #Calculate the amount of stock equity sold and update it 
                    StockWallet_instance.save(commit=False)
                        
                    
                    WalletTransaction_instance = WalletTransaction(amount1, amount3)
                    Wallet_instance = Wallet.objects.filter(user=name).last()
                    Wallet_instance.user = name
                    Wallet_instance.stock_eq = WalletTransaction_instance.sell_stock_eq_update(amount2)
                    Wallet_instance.balance = WalletTransaction_instance.sell_balance_update(amount2)
                    Wallet_instance.save(commit=False)     #Updates the user's wallet

                    Sell.objects.create(user = name, name = stock_name, sold = True, total_selling_amount = amount2,
                        stock_selling_price = stock_price, shares = shares_left)
                    
                    StockWallet_instance.save()
                    Wallet_instance.save()
                    data2.delete()                      #Deletes the specific amount instance to save space
                    data.delete()
                    return redirect('payment:done')
                else:
                    return redirect('payment:canceled')    
    
    return render(request, 'stock_sell.html', {'Sell': Sell, 'form': form, 'total': StockWallet_instance.shares, 'prices': stock_price, 'stock': stock_name })


#TRADING VIEWS
@login_required
def long_position(request):
    form = LongForm(request.POST)
#    sign = True
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    user_name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    #PRICE FETCHING
    data =  price_db.objects.filter(user=user_name).last()                #Gets the most recent price entry in the price_db database as a queryset
    balances = Wallet.objects.filter(user=user_name).last()             #Balance left in the account
    
    #DATA EXTRACTION
    open_price = float(data.openprice)                              #Strips and assings the open price value from price_db as a float data type
    close_price = float(data.closeprice)
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
    ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    amount1 = float(balances.balance)                         #Assigns the wallet balance as a float data type   

    
    if request.method == "POST":
        if form.is_valid():
            Amount = form.save(commit=False)
            Amount.user = request.user.username
            Amount.save()

            sum_price = float(Amount.total_price)                                   # amount user wants to trade
            otp = Amount.otp                                                        # otp code
            leverage_used = Amount.leverage                                              # Leverage used          
            
            #Instance declaration
            Trading_instance = Trading(amount1, leverage_used)
            
            if totp.verify(otp):
                Long.objects.create(user = user_name, name = stock_name, ticker = ticker, amount = sum_price, 
                    leverage = leverage_used, current_price = close_price, long_price = open_price, 
                    returns = Trading_instance.long_position(sum_price, open_price, close_price))

                balances.balance -= sum_price
                balances.save()
                data.delete()

                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
        
    return render(request, 'stock_long.html', {'Sell': Sell, 'form': form,  'total': balances.balance, 'prices': open_price, 'stock': stock_name })


@login_required
def short_position(request):
    form = ShortForm(request.POST)
#    sign = False
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    user_name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    #PRICE FETCHING
    data = price_db.objects.filter(user=user_name).last()                #Gets the most recent price entry in the price_db database as a queryset
    balances = Wallet.objects.filter(user=user_name).last()              #Balance left in the account
    
    #DATA EXTRACTION
    open_price = float(data.openprice)                             #Strips and assings the open price value from price_db as a float data type
    close_price = float(data.closeprice)
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
    ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    amount1 = float(balances.balance)                         #Assigns the wallet balance as a float data type   
    
    
    if request.method == "POST":
        if form.is_valid():
            Amount = form.save(commit=False)
            Amount.user = request.user.username
            Amount.save()
            
            sum_price = float(Amount.total_price)                                   # amount user wants to trade
            otp = Amount.otp                                                        # otp code
            leverage_used = Amount.leverage                                              # Leverage used          
            Trading_instance = Trading(amount1, leverage_used)
            
            if totp.verify(otp):
                Short.objects.create(user = user_name, name = stock_name, amount = sum_price, ticker = ticker, 
                    leverage = leverage_used, current_price = close_price, short_price = open_price, 
                    returns = Trading_instance.short_position(sum_price, open_price, close_price))
                
                balances.balance -= sum_price
                balances.save()

                data.delete()
                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
        
    return render(request, 'stock_short.html', {'Sell': Sell, 'form': form,  'total': balances.balance, 'prices': open_price, 'stock': stock_name })
