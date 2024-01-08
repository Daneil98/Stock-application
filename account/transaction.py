from django.conf import settings
from payment.models import Payment, Buy, Sell
from .models import Profile, price_db
from django.db.models import Sum


"""
cost = price_db.objects.order_by('-id').first()               #Gets the most recent price entry in the price_db database as a queryset
costs = cost.values('price')                                    #Strips the price from the queryset response
prices = float(costs[0]['price'])                               #Assigns the price as a float data type so it can be used in arithmetic operations
"""


class BuyTransaction():
    def __init__(self, balance, shares=0.0):
        self.balance = balance
        self.shares = shares
        
    def share_number(self, total_purchase_price, price):                  #This function calculates the number of shares bought
        numbers = total_purchase_price / price
        self.shares += numbers
        shares = self.shares
        return shares
        
    def get_balance(self):              #This function returns the account balance 
        return self.balance
        
    def charge(self, amount, shares):                #This function is what is run when the user wants to buy a stock
        if amount > self.balance:
            print("Insufficient funds")
            return False
        else:
            self.balance -= (amount * shares)
            print("Sufficient Funds")
            return self.balance
  
            
class SellTransaction():
    def __init__(self, balance, shares=0.0):
        self.balance = balance
        self.shares = shares
          
    def share_number(self, total_selling_amount, price):                  #This function calculates the number of shares bought
        numbers = total_selling_amount / price
        self.shares += numbers
        shares = self.shares
        return shares
        
    def get_balance(self):              #This function returns the account balance 
        return self.balance
    
    def sell(self, price):              #This function is run when the user wants to sell a stock
        self.balance += price
        
