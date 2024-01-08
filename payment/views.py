
import braintree
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import DepositForm, BuyForm, SellForm
from .models import Payment, Buy, Sell, amount
from account.models import price_db, Profile

from django.http import HttpResponse, HttpResponseRedirect
from account.transaction import BuyTransaction, SellTransaction
from account.tiingo import get_meta_data, get_price

# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

#DEPOSIT VIEWS
def payment_process(request):
    Payment_id = request.session.get('Payment_id')
    Payment_instance = Payment()
    total_cost = Payment_instance.amount
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
            # mark the order as paid
            Payment_instance.paid = True
            # store the unique transaction id
            Payment_instance.braintree_id = result.transaction.id
            #CHeck for duplicate transactions
            Payment.transaction_id = result.transaction.id
            # save the payment
            Payment_instance.save()
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
    prices = float(data.price)                                        #Strips and assigns the price value as a float data type so it can be used in arithmetic operations
    stock_name = str(data.name)                                       #Strips and assigns the name value as a string data type
    profile = request.user
    name = profile.username
    
    total = Payment.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum']           #Total amount of successful deposits
    amount1 = float(total)              #Assigns total deposits as a float data type 
    amount2 = float(prices)             #Current price of the stock to be purchased
    amount3 = Sell.selling_amount       #Current price of the stock to be sold
    
    amount_instance = amount() 
    if request.method == "POST":
        if form.is_valid():
            form.save()
        total_amount = amount.objects.order_by('-id').first()
        sum_price = float(total_amount.total_purchase_price)
        
        Transaction_instance = BuyTransaction(amount1)                     #Creates a transaction instance for the transaction class witn amount1 as a data input
        shares_bought = Transaction_instance.share_number(sum_price, amount2)
        if Transaction_instance.charge(amount2, shares_bought):
            Buy_instance = Buy()
            Buy_instance.user = name
            Buy_instance.name = stock_name
            Buy_instance.bought = True
            Buy_instance.stock_purchase_price = amount2
            Buy_instance.total_purchase_amount = sum_price
            Buy_instance.shares = shares_bought
            Buy_instance.balance = Transaction_instance.get_balance()
            Buy_instance.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    
    return render(request, 'stock_buy.html', {'Buy': Buy, 'form': form, 'total': amount1, 'prices': prices, 'stock': stock_name })
            
            
def stock_sell(request, **ticker):
    form = SellForm(request.POST)
    data = price_db.objects.order_by('-id').first()                   #Gets the most recent price entry in the price_db database as a queryset
    prices = float(cost.price)                                        #Strips and assigns the price value as a float data type so it can be used in arithmetic operations
    stock_name = str(cost.name)                                       #Strips and assigns the name value as a string data type
    profile = request.user
    name = profile.username
    
    total = Payment.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum']           #Total amount of successful deposits
    amount1 = float(total)              #Assigns total deposits as a float data type 
    amount2 = float(prices)             #Current price of the stock to be purchased
    amount3 = Sell.selling_amount       #Current price of the stock to be sold
    
    amount_instance = amount() 
    if request.method == "POST":
        if form.is_valid():
            form.save()
        total_amount = amount.objects.order_by('-id').first()
        sum_price = float(total_amount.total_purchase_price)
        
        Transaction_instance = Transaction(amount1)                     #Creates a transaction instance for the transaction class witn amount1 as a data input
        shares_bought = Transaction_instance.share_number(sum_price, amount2)
        if Transaction_instance.charge(amount2, shares_bought):
            Buy_instance = Buy()
            Buy_instance.user = name
            Buy_instance.name = stock_name
            Buy_instance.bought = True
            Buy_instance.stock_purchase_price = amount2
            Buy_instance.total_purchase_price = sum_price
            Buy_instance.shares = shares_bought
            Buy_instance.balance = Transaction_instance.get_balance()
            Buy_instance.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    
    return render(request, 'stock_buy.html', {'Buy': Buy, 'form': form, 'total': amount1, 'prices': prices, 'stock': stock_name })
            
            