import braintree
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import BuyForm, SellForm
from .models import Payment, Buy, Sell, amount, Wallet, Stock_Wallet
from account.models import Profile, price_db
from django.urls import reverse
from payment.transaction import BuyTransaction, SellTransaction, WalletTransaction, StockHolding
from django.contrib.auth.decorators import login_required
import pyotp
    
# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


#DEPOSIT VIEWS
@login_required
def payment_process(request):
    Payment_id = request.session.get('Payment_id')
    Payment_instance = Payment()
    total_cost = Payment_instance.amount
    profile = request.user
    name = profile.username
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': 'fake-valid-nonce',
            "options" : {
                "submit_for_settlement": True, # Required
            },  
        })
        
        # create and submit transaction
        if result.is_success:
            
            Payment_instance = Payment()
            Payment_instance.user = name
            # mark the order as paid
            Payment_instance.paid = True
            # store the unique transaction id
            Payment_instance.braintree_id = result.transaction.id
            #CHeck for duplicate transactions
            Payment.transaction_id = result.transaction.id
            # save the payment
            Payment_instance.save()
            
            data = Payment.objects.order_by('-id').first()
            deposit = float(data.amount)
            Wallet_instance = Wallet()
            Wallet_instance.balance = deposit
            Wallet_instance.stock_eq = 0.00
            Wallet_instance.user = name
            Wallet_instance.save()
            
            return redirect('payment:done')
        else:
            print(result.message)
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
def stock_buy(request, **ticker):
    
    #GETS THE USER'S DATA
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    name = user.username
    secret = profile.secret_key
    totp = pyotp.TOTP(secret)
    
    # PRICE FETCHING
    balance = Wallet.objects.order_by('-id').first()       #Balance left in the account
    form = BuyForm(request.POST)
    data = price_db.objects.filter(user=name).order_by('-id').first()            #Gets the most recent price entry in the price_db database as a queryset
    prices = float(data.closeprice)                                   #Strips the close-price from the price_db and declares it as a float data type so it can be used in arithmetic operations
    stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
    
    
    amount1 = float(balance.balance)     #Assigns the wallet balance as a float data type 
    amount3 = float(balance.stock_eq)    #Current stock equity in the wallet assigned
    amount2 = float(prices)             #Current price of the stock to be purchased

    
    if request.method == "POST":
        if form.is_valid():
            Amount = form.save(commit=False)
            Amount.user = request.user.username
            Amount.save()
        else:
            print("Error")
            raise ValueError

        total_amount = amount.objects.filter(user=name).order_by('-id').first()
        price = total_amount.total_price
        sum_price = float(price)
        otp = total_amount.otp
        
        
        #Instance declarations
        WalletTransaction_instance = WalletTransaction(amount1, amount3)
        Transaction_instance = BuyTransaction(amount1)                     #Creates a transaction instance for the transaction class with amount1 as the self.balance
        shares_bought = Transaction_instance.share_number(sum_price, amount2)
        
        
        if Transaction_instance.charge(amount2, shares_bought) and totp.verify(otp):
            Buy_instance = Buy()
            Wallet_instance = Wallet()
            try:
                StockWallet_instance = Stock_Wallet.objects.get(name=stock_name)
                stock_equity = StockWallet_instance.equity
                StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                StockWallet_instance.user = name
                StockWallet_instance.name = stock_name
                shares =  StockWallet_instance.shares               #stocks shares present before current transaction 
                StockWallet_instance.shares = StockHoldingTransaction_instance.buy_shares(shares, shares_bought)            #Calculate the number of shares added and update it 
                StockWallet_instance.equity = StockHoldingTransaction_instance.buy_stock_eq_update(sum_price)               #Calculate the amount of stock equity added and update it 
                StockWallet_instance.save()
                
            except Stock_Wallet.DoesNotExist:
                StockWallet_instance = Stock_Wallet()
                shares =  0   
                stock_equity = 0
                
                StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                StockWallet_instance.user = name
                StockWallet_instance.name = stock_name
                StockWallet_instance.shares = StockHoldingTransaction_instance.buy_shares(shares, shares_bought)           #Calculate the number of shares added and update it 
                StockWallet_instance.equity = StockHoldingTransaction_instance.buy_stock_eq_update(sum_price)              #Calculate the amount of stock equity added and update it 
                StockWallet_instance.save()
                
                
            Buy_instance.user = name
            Buy_instance.name = stock_name
            Buy_instance.bought = True
            Buy_instance.stock_purchase_price = amount2
            Buy_instance.total_purchase_amount = sum_price
            Buy_instance.shares = shares_bought
            Buy_instance.save()
            
            
            WalletTransaction_instance = WalletTransaction(amount1, amount3)
            Wallet_instance.user = name
            Wallet_instance.balance = WalletTransaction_instance.buy_balance_update(sum_price)           
            Wallet_instance.stock_eq = WalletTransaction_instance.buy_stock_eq_update(sum_price)
            Wallet_instance.save() 
            
            total_amount.delete()
            data.delete()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    
    return render(request, 'stock_buy.html', {'Buy': Buy, 'form': form, 'total': amount1, 'prices': prices, 'stock': stock_name })
    
    
            
@login_required        
def stock_sell(request, **ticker):
    
    #GETS THE USER'S NAME
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    name = user.username
    secret = profile.secret_key
    totp = pyotp.TOTP(secret)
    
    form = SellForm(request.POST)
    
    #BASIC STOCKDATA FROM TICKER PAGE
    data = price_db.objects.filter(user=name).order_by('-id').first()                #Gets the most recent price entry in the price_db database as a queryset
    stock_price = float(data.openprice)                            #Srips and assings the open price value from price_db as a float data type
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
    
    #STOCK DATA FROM THE BUY MODEL DB
    StockWallet_instance = Stock_Wallet.objects.get(name=stock_name)
    stock_name1 = str(StockWallet_instance.name)
    

    
    #BASIC DATA FROM THE WALLET MODEL DB
    balance = Wallet.objects.filter(user=name).order_by('-id').first()       #Balance left in the account
    amount1 = wallet_balance = float(balance.balance)      #Assigns the wallet balance as a float data type 
    amount3 = wallet_eq_balance = float(balance.stock_eq)           
    
    shares_avail = (StockWallet_instance.shares)
    
    if stock_name == stock_name1:  
        if request.method == "POST":
            if form.is_valid():
                Amount = form.save(commit=False)
                Amount.user = request.user.username
                Amount.save()
            else:
                print("Error")
                raise ValueError
            
            data2 = amount.objects.filter(user=name).order_by('-id').first()

            sum_price = data2.total_price
            amount2 = float(sum_price)
            otp = data2.otp
            Transaction_instance = SellTransaction(amount1)                     #Creates a transaction instance for the transaction class witn amount1 as a data input
            
            WalletTransaction_instance = WalletTransaction(wallet_balance, wallet_eq_balance)
            shares_left = Transaction_instance.share_number(amount2, stock_price)
            
            
            if Transaction_instance.sell(amount2, amount3)and totp.verify(otp):
                Sell_instance = Sell()
                Wallet_instance = Wallet()                
                

                StockWallet_instance = Stock_Wallet.objects.get(name=stock_name)        #Retrieve stock wallet entry/instance by it's stock name
                stock_equity = StockWallet_instance.equity

                StockHoldingTransaction_instance = StockHolding(amount1, stock_equity)
                StockWallet_instance.user = name
                StockWallet_instance.name = stock_name
                StockWallet_instance.shares = StockHoldingTransaction_instance.sell_shares(shares_left, shares_avail)               #Calculate the number of shares sold and update it 
                StockWallet_instance.equity = StockHoldingTransaction_instance.sell_stock_eq_update(amount2)                        #Calculate the amount of stock equity sold and update it 
                StockWallet_instance.save()
                    
                
                Sell_instance.user = name
                Sell_instance.name = stock_name
                Sell_instance.sold = True
                Sell_instance.total_selling_amount = amount2
                Sell_instance.stock_selling_price = stock_price
                Sell_instance.shares = shares_left
                Sell_instance.save()
                
                
                WalletTransaction_instance = WalletTransaction(amount1, amount3)
                Wallet_instance.user = name
                Wallet_instance.stock_eq = WalletTransaction_instance.sell_stock_eq_update(amount2)
                Wallet_instance.balance = WalletTransaction_instance.sell_balance_update(amount2) 
                Wallet_instance.save()
                
                data2.delete()                      #Deletes the specific amount instance to save space
                data.delete()
                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
    return render(request, 'stock_sell.html', {'Sell': Sell, 'form': form, 'total': shares_avail, 'prices': stock_price, 'stock': stock_name })