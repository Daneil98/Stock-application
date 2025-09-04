from django.test import TestCase

from .transaction import WalletTransaction

# Create your tests here.

balance = float(10000)
stock_eq = float(0.0)


leverage = int(3)
amount = float(100)
current_price = float(120.00)
long_price = float(100.00)
short_price = float(100.00)


#Transaction_instance = Trading(balance, leverage)

#Transaction_instance.buy_balance_update(100)
#Transaction_instance.buy_stock_eq_update(100)


#Transaction_instance.long_position(amount, long_price, current_price)
#Transaction_instance.short_position(amount, short_price, current_price)

#print(Transaction_instance.balance, Transaction_instance.stock_eq)