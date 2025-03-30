from celery import shared_task
from .models import *
from account.models import *
from .transaction import *
from django.core.exceptions import ObjectDoesNotExist
import requests



headers = {
        'Content-Type': 'application/json',
    }



@shared_task
def get_wallet_data(user_name):
    #Fetch wallet data.
    return Wallet.objects.filter(user=user_name).last()

@shared_task
def get_stock_wallet(user_name, stock_name):
    #Fetch wallet data.
    return Stock_Wallet.objects.filter(user=user_name, name=stock_name).last()


@shared_task
def get_latest_price(user_name):
    #Fetch the latest stock price for the user.
    return price_db.objects.filter(user=user_name).last()

@shared_task
def update_stock_wallet(stock_wallet, shares, sum_price, sign):
    #Update or create stock wallet.

    if sign == True:
        stock_wallet.shares = (stock_wallet.shares or 0) + shares
        stock_wallet.equity += sum_price
        stock_wallet.save(commit=False)
        
    else:
        stock_wallet.shares -= shares
        stock_wallet.equity -= sum_price
        stock_wallet.save(commit=False)
    
        
@shared_task
def create_trade(wallet, user_name, stock_name, ticker, leverage, sum_price, close_price, open_price, balance, sign):
    #create Trade
    Trading_instance = Trading(balance, leverage)                      #Creates a transaction instance
    
    if sign == True:    
        Long.objects.create(user = user_name, name = stock_name, ticker = ticker, amount = sum_price, leverage = leverage, 
            current_price = close_price, long_price = open_price, returns = Trading_instance.long_position(sum_price, open_price, close_price)
        )
        
        wallet.balance -= sum_price
        wallet.save(commit=False)
        
    else:
        Short.objects.create(user = user_name, name = stock_name, ticker = ticker, amount = sum_price, leverage = leverage, 
            current_price = close_price, short_price = open_price, returns = Trading_instance.long_position(sum_price, open_price, close_price)
        )
        
        wallet.balance -= sum_price
        wallet.save(commit=False)
     
     
@shared_task
def update_wallet(wallet, balance, stock_eq, sum_price, sign):
    #Update wallet balance and stock equity.

    
    if wallet:
        if sign == True:
            WalletTransaction_instance = WalletTransaction(balance, stock_eq)
            wallet.balance = WalletTransaction_instance.buy_balance_update(sum_price)           
            wallet.stock_eq = WalletTransaction_instance.buy_stock_eq_update(sum_price)
            wallet.save(commit=False)
        
        else:
            WalletTransaction_instance = WalletTransaction(balance, stock_eq)
            wallet.balance = WalletTransaction_instance.sell_balance_update(sum_price)           
            wallet.stock_eq = WalletTransaction_instance.sell_stock_eq_update(sum_price)
            wallet.save(commit=False)
        

@shared_task
def payment(user_name, result):
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



# AUTOMATIC CUSTOMER TRADES UPDATE


def get_price(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?token=ade8eea34c1658569b3997046a22003af1a3ad08".format(ticker), headers=headers)
    ans = requestResponse.json()
    close = ans[0]['close']
    return close
   

@shared_task
def update_long():
    
    users = Profile.objects.order_by('user').all()
    
    for user in users:
        name = user.user.username 
        balance = Wallet.objects.filter(user=name).last()
        trades = Long.objects.filter(user=name).all()
        
        for trade in trades:
            long_price = trade.long_price
            leverage = trade.leverage
            amount = trade.amount
            
            current_price = get_price(trade.ticker)
            
            trade_update = Trading(balance, leverage)
            trade.returns = trade_update.long_position(amount, long_price, current_price)
            trade.current_price = current_price
            trade.save()
            print(current_price)
            print(trade.returns)
        
        
@shared_task    
def update_short():
    
    users = Profile.objects.order_by('user').all()
    
    for user in users:
        name = user.user.username    
        trades = Short.objects.filter(user=name).all()
        balance = Wallet.objects.filter(user=name).last()
        
        for trade in trades:
            short_price = trade.short_price
            leverage = trade.leverage
            amount = trade.amount
            
            current_price = get_price(trade.ticker)
            
            trade_update = Trading(balance, leverage)
            returns = trade_update.short_position(amount, short_price, current_price)
            trade.current_price = current_price
            trade.returns = returns
            trade.save()
            print(current_price)
            print(trade.returns)

    
    
