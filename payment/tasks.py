from celery import shared_task
from .models import *
from account.models import *
from .transaction import *
from django.core.exceptions import ObjectDoesNotExist



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
def update_stock_wallet(user_name, stock_name, shares, sum_price, sign):
    #Update or create stock wallet.

    if sign == True:
        stock_wallet, created = Stock_Wallet.objects.get_or_create(user=user_name, name=stock_name)
        stock_wallet.shares = (stock_wallet.shares or 0) + shares
        stock_wallet.equity += sum_price
        stock_wallet.save()
        
    else:
        stock_wallet = Stock_Wallet.objects.filter(user=user_name, name=stock_name).last()
        stock_wallet.shares -= shares
        stock_wallet.equity -= sum_price
        stock_wallet.save()
    
        
@shared_task
def create_trade(user_name, stock_name, ticker, leverage, sum_price, close_price, open_price, balance, sign):
    #create Trade
    Trading_instance = Trading(balance, leverage)                      #Creates a transaction instance
    wallet = Wallet.objects.filter(user=user_name).last()
    
    if sign == True:    
        Long.objects.create(user = user_name, name = stock_name, ticker = ticker, amount = sum_price, leverage = leverage, 
            current_price = close_price, long_price = open_price, returns = Trading_instance.long_position(sum_price, open_price, close_price)
        )
        
        wallet.balance -= sum_price
        wallet.save()
        
    else:
        Short.objects.create(user = user_name, name = stock_name, ticker = ticker, amount = sum_price, leverage = leverage, 
            current_price = close_price, short_price = open_price, returns = Trading_instance.long_position(sum_price, open_price, close_price)
        )
        
        wallet.balance -= sum_price
        wallet.save()
     
     
@shared_task
def update_wallet(user_name, balance, stock_eq, sum_price, sign):
    #Update wallet balance and stock equity.
    wallet = Wallet.objects.filter(user=user_name).last()
    
    if wallet:
        if sign == True:
            WalletTransaction_instance = WalletTransaction(balance, stock_eq)
            wallet.balance = WalletTransaction_instance.buy_balance_update(sum_price)           
            wallet.stock_eq = WalletTransaction_instance.buy_stock_eq_update(sum_price)
            wallet.save()
        
        else:
            WalletTransaction_instance = WalletTransaction(balance, stock_eq)
            wallet.balance = WalletTransaction_instance.sell_balance_update(sum_price)           
            wallet.stock_eq = WalletTransaction_instance.sell_stock_eq_update(sum_price)
            wallet.save()
        

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
        # save the payment
        Payment_instance.save()
        
        Wallet_instance = Wallet.objects.filter(user=user_name).last()
        Wallet_instance.balance += amount
        Wallet_instance.user = user_name
        Wallet_instance.save()



    
    
