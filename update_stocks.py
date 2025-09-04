import requests
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_stock.settings')
django.setup()
from account.models import Profile
from payment.transaction import Trading
from payment.models import Long, Short, Wallet

#THIS SCRIPT IS TO UPDATE ALL USERS TRADES EVERYDAY OR WHEN IT IS RUN
headers = {
        'Content-Type': 'application/json',
    }


def get_price(ticker):
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?token=ade8eea34c1658569b3997046a22003af1a3ad08".format(ticker), headers=headers)
    ans = requestResponse.json()
    close = ans[0]['close']
    return close
   


def update_long():

    users = Profile.objects.order_by('user').all()
    
    for user in users:
        name = user.user.username 
        trades = Long.objects.filter(user=name).all()
        balance = Wallet.objects.filter(user=name).last()
    
        for trade in trades:
            long_price = float(trade.long_price)
            leverage = int(trade.leverage)
            amount = float(trade.amount)
            
            current_price = get_price(trade.ticker)
            
            trade_update = Trading(balance, leverage)
            returns = trade_update.long_position(amount, long_price, current_price)
            trade.current_price = current_price
            trade.returns = returns
            trade.save()
            print(current_price)
            print(trade.returns)
        
    
def update_short():
    
    users = Profile.objects.order_by('user').all()
    
    for user in users:
        name = user.user.username    
        trades = Short.objects.filter(user=name).all()
        balance = Wallet.objects.filter(user=name).last()
        
        for trade in trades:
            short_price = float(trade.short_price)
            leverage = int(trade.leverage)
            amount = float(trade.amount)
            
            current_price = get_price(trade.ticker)
            
            trade_update = Trading(balance, leverage)
            returns = trade_update.short_position(amount, short_price, current_price)
            trade.current_price = current_price
            trade.returns = returns
            trade.save()
            print(current_price)
            print(trade.returns)


update_long()
update_short()


"""
from myapp.tasks import sample_task
sample_task.delay()

celery -A project worker --loglevel=info

"""