
import braintree
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import DepositForm, BuyForm, SellForm
from .models import Payment, Buy, Sell, amount, Wallet, Stock_Wallet
from account.models import price_db
from django.urls import reverse
from payment.transaction import BuyTransaction, SellTransaction, WalletTransaction, StockHolding
from account.tiingo import get_meta_data, get_price
    
# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

#DEPOSIT VIEWS
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

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')



#STOCK BUY & SELL VIEWS
def stock_buy(request, **ticker):
    form = BuyForm(request.POST)
    
    data = price_db.objects.order_by('-id').first()                   #Gets the most recent price entry in the price_db database as a queryset
    prices = float(data.closeprice)                                   #Strips the close-price from the price_db and declares it as a float data type so it can be used in arithmetic operations
    stock_name = str(data.name)                                       #Strips and declares the name value as a string data type
    
    #GETS THE USER'S NAME
    profile = request.user
    name = profile.username
    balance = Wallet.objects.order_by('-id').first()       #Balance left in the account
    
    amount1 = float(balance.balance)      #Assigns the wallet balance as a float data type 
    amount3 = float(balance.stock_eq)    
    amount2 = float(prices)             #Current price of the stock to be purchased
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
        total_amount = amount.objects.order_by('-id').first()
        price = total_amount.total_price
        sum_price = float(price)
        
         
        WalletTransaction_instance = WalletTransaction(amount1, amount3)
        Transaction_instance = BuyTransaction(amount1)                     #Creates a transaction instance for the transaction class witn amount1 as the self.balance
        StockHoldingTransaction_instance = StockHolding(amount1, amount3)
        shares_bought = Transaction_instance.share_number(sum_price, amount2)
        
        
        #total_equity_in_buy = float(Buy.objects.filter(bought=True).aggregate(Sum('equity'))['equity__sum'])
        
        
        if Transaction_instance.charge(amount2, shares_bought):
            Buy_instance = Buy()
            Wallet_instance = Wallet()
            StockWallet_instance = Stock_Wallet()
            
            totalH = Buy.objects.filter(bought=True).aggregate(Sum('shares'))['shares__sum']
            
            if totalH is None:    
                total_shares_in_buy = 0.00
                StockWallet_instance.user = name
                StockWallet_instance.name = stock_name
                StockWallet_instance.equity = sum_price
                StockWallet_instance.shares = StockHoldingTransaction_instance.buy_shares(shares_bought, total_shares_in_buy)
                StockWallet_instance.save()
                
            else:
                totalH1 = float(totalH)
                total_shares_in_buy = totalH1
                StockWallet_instance.user = name
                StockWallet_instance.name = stock_name
                StockWallet_instance.equity = StockHoldingTransaction_instance.buy_stock_eq_update(sum_price)
                StockWallet_instance.shares = StockHoldingTransaction_instance.buy_shares(shares_bought, total_shares_in_buy)
                StockWallet_instance.save()
            
            
            
            Buy_instance.user = name
            Buy_instance.name = stock_name
            Buy_instance.bought = True
            Buy_instance.stock_purchase_price = amount2
            Buy_instance.total_purchase_amount = sum_price
            Buy_instance.shares = shares_bought
            Buy_instance.save()
            
           
            Wallet_instance.user = name
            Wallet_instance.balance = WalletTransaction_instance.buy_balance_update(sum_price)           
            Wallet_instance.stock_eq = WalletTransaction_instance.buy_stock_eq_update(sum_price)
            Wallet_instance.save() 
            
            
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    
    return render(request, 'stock_buy.html', {'Buy': Buy, 'form': form, 'total': amount1, 'prices': prices, 'stock': stock_name })
            
            
def stock_sell(request, **ticker):
    form = SellForm(request.POST)
    
    #BASIC STOCKDATA FROM TICKER PAGE
    data = price_db.objects.order_by('-id').first()                 #Gets the most recent price entry in the price_db database as a queryset
    stock_price = float(data.openprice)                             #Srips and assings the open price value from price_db as a float data type
    stock_name = str(data.name)                                     #Strips and assigns the name value as a string data type
    
    #STOCK DATA FROM THE BUY MODEL DB
    data1 = Buy.objects.order_by('-id').first()
    stock_name1 = str(data1.name)
    
    #GETS THE USER'S NAME
    profile = request.user
    name = profile.username
    
    #BASIC DATA FROM THE WALLET MODEL DB
    balance = Wallet.objects.order_by('-id').first()       #Balance left in the account
    amount1 = wallet_balance = float(balance.balance)      #Assigns the wallet balance as a float data type 
    amount3 = wallet_eq_balance = float(balance.stock_eq)            
    avail = Stock_Wallet.objects.order_by('-id').first()
    shares_avail = float(avail.shares)
    
    
    
    if stock_name == stock_name1:  
        if request.method == "POST":
            if form.is_valid():
                form.save()
            else:
                print("Error")
                raise ValueError
            
            data2 = amount.objects.order_by('-id').first()
            sum_price = data2.total_price
            amount2 = float(sum_price)
            Transaction_instance = SellTransaction(amount1)                     #Creates a transaction instance for the transaction class witn amount1 as a data input
            
            WalletTransaction_instance = WalletTransaction(wallet_balance, wallet_eq_balance)
            shares_left = Transaction_instance.share_number(amount2, stock_price)
            
            if Transaction_instance.sell(amount2, amount3):
                Sell_instance = Sell()
                Wallet_instance = Wallet()
                StockWallet_instance = Stock_Wallet()
                StockHoldingTransaction_instance = StockHolding(amount1, amount3)
                
                Sell_instance.user = name
                Sell_instance.name = stock_name
                Sell_instance.sold = True
                Sell_instance.total_selling_amount = amount2
                Sell_instance.stock_selling_price = stock_price
                Sell_instance.shares = shares_left
                Sell_instance.save()
                
                StockWallet_instance.user = name
                StockWallet_instance.name = stock_name
                StockWallet_instance.shares = StockHoldingTransaction_instance.sell_shares(shares_left, shares_avail)
                StockWallet_instance.equity = StockHoldingTransaction_instance.sell_stock_eq_update(amount2)
                StockWallet_instance.save()
                
                
                Wallet_instance.user = name
                Wallet_instance.stock_eq = WalletTransaction_instance.sell_stock_eq_update(amount2)
                Wallet_instance.balance = WalletTransaction_instance.sell_balance_update(amount2) 
                Wallet_instance.save()
                return redirect('payment:done')
            else:
                return redirect('payment:canceled')
    return render(request, 'stock_sell.html', {'Sell': Sell, 'form': form, 'total': shares_avail, 'prices': stock_price, 'stock': stock_name })