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
    name = request.user.username
    
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

            payment(name, result)                 # A celery task
            
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
    sign = True                                     # Helps determine what kind of operation is ongoing
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    # PRICE FETCHING
    balance = get_wallet_data(name)         #Balance left in the account
    data = get_latest_price(name)           #Gets the most recent price entry in the price_db database 
    
    #DATA EXTRACTION
    prices = float(data.closeprice)                                   #Strips the close-price from the price_db and declares it as a float data type so it can be used in arithmetic operations
    stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
#   ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    wallet_balance = float(balance.balance)                        #Assigns the wallet balance as a float data type 
    stock_eq = float(balance.stock_eq)                       #Current stock equity in the wallet assigned

    
    if request.method == "POST":
        if form.is_valid():
            total_amount = form.save(commit=False)
            total_amount.user = name
            total_amount.save()
            
            sum_price = float(total_amount.total_price)
            otp = total_amount.otp
            shares_bought = float(sum_price / prices)
            
            if totp.verify(otp):
                wallet = Wallet.objects.filter(user=name).last()
                update_stock_wallet(name, stock_name, shares_bought, sum_price, sign)               #celery task updates the user's stock wallet
                
                stock_wallet, created = Stock_Wallet.objects.get_or_create(user=name, name=stock_name)
                update_wallet(name, wallet_balance, stock_eq, sum_price, sign)                       #celery task updates the user's wallet
                
                Buy.objects.create(user = name, name = stock_name, bought = True,                   #Documents the user's purchase
                    stock_purchase_price = prices, total_purchase_amount = sum_price, shares = shares_bought)              
                
                stock_wallet.save()
                wallet.save()
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
    user_name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    #PRICE FETCHING
    data = get_latest_price(user_name)                #Gets the most recent price entry in the price_db database as a queryset
    balance = get_wallet_data(user_name)              #Balance left in the account
    
    #DATA EXTRACTION
    stock_price = float(data.openprice)                             #Strips and assings the open price value from price_db as a float data type
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
#   ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    wallet_balance = float(balance.balance)                         #Assigns the wallet balance as a float data type 
    wallet_eq_balance = float(balance.stock_eq)           
    
    
    #STOCK DATA FROM THE BUY MODEL DB
    StockWallet_instance = get_stock_wallet(user_name, stock_name)

    if StockWallet_instance is None:
        return redirect('my_stocks')

    if request.method == "POST":
        if stock_name == StockWallet_instance.name:
            if form.is_valid():
                data2 = form.save(commit=False)
                data2.user = user_name
                data2.save()

                sum_price = float(data2.total_price)                                          # Equity user wants to sell
                otp = data2.otp                                                               # otp code
                
                shares_sell = float(sum_price/stock_price)                                    #Calculates the number of shares to be sold
                
                if totp.verify(otp):
                    update_stock_wallet(StockWallet_instance, user_name, stock_name, shares_sell, sum_price, sign)          #Updates the user's stock_wallet
                    wallet = Wallet.objects.filter(user=user_name).last()
                    Sell.objects.create(user = user_name, name = stock_name, #ticker=ticker,                  #Documents the user's sale
                        sold = True, total_selling_amount = sum_price, stock_selling_price = stock_price, 
                        shares = shares_sell)
                    
                    update_wallet(wallet, user_name, wallet_balance, wallet_eq_balance, sum_price, sign)      #Updates the user's wallet


                    StockWallet_instance.save()
                    wallet.save()
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
    sign = True
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    user_name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    #PRICE FETCHING
    data = get_latest_price(user_name)                #Gets the most recent price entry in the price_db database as a queryset
    balance = get_wallet_data(user_name)              #Balance left in the account
    
    #DATA EXTRACTION
    open_price = float(data.openprice)                             #Strips and assings the open price value from price_db as a float data type
    close_price = float(data.closeprice)
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
    ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    wallet_balance = float(balance.balance)                         #Assigns the wallet balance as a float data type   

    
    if request.method == "POST":
        if form.is_valid():
            Amount = form.save(commit=False)
            Amount.user = request.user.username
            Amount.save()

            sum_price = float(Amount.total_price)                                   # amount user wants to trade
            otp = Amount.otp                                                        # otp code
            leverage = Amount.leverage                                              # Leverage used          
            
            
            if totp.verify(otp):
                wallet = Wallet.objects.filter(user=user_name).last()
                create_trade(wallet, user_name, stock_name, ticker, leverage, sum_price, close_price, open_price, balance, sign)

                wallet.save()
                Amount.delete()
                data.delete()
                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
        
    return render(request, 'stock_long.html', {'Sell': Sell, 'form': form,  'total': wallet_balance, 'prices': open_price, 'stock': stock_name })


@login_required
def short_position(request):
    form = ShortForm(request.POST)
    sign = False
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    user_name = user.username
    totp = pyotp.TOTP(profile.secret_key)
    
    #PRICE FETCHING
    data = get_latest_price(user_name)                #Gets the most recent price entry in the price_db database as a queryset
    balance = get_wallet_data(user_name)              #Balance left in the account
    
    #DATA EXTRACTION
    open_price = float(data.openprice)                             #Strips and assings the open price value from price_db as a float data type
    close_price = float(data.closeprice)
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
    ticker = str(data.ticker)                                       #Strips and assigns the ticker as a string
    wallet_balance = float(balance.balance)                         #Assigns the wallet balance as a float data type   
    
    
    if request.method == "POST":
        if form.is_valid():
            Amount = form.save(commit=False)
            Amount.user = request.user.username
            Amount.save()
            
            sum_price = float(Amount.total_price)                                   # amount user wants to trade
            otp = Amount.otp                                                        # otp code
            leverage = Amount.leverage                                              # Leverage used          
            
            if totp.verify(otp):
                wallet = Wallet.objects.filter(user=user_name).last()
                create_trade(wallet, user_name, stock_name, ticker, leverage, sum_price, close_price, open_price, balance, sign)
                
                wallet.save()
                Amount.delete()
                data.delete()
                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
        
    return render(request, 'stock_short.html', {'Sell': Sell, 'form': form,  'total': wallet_balance, 'prices': open_price, 'stock': stock_name })
