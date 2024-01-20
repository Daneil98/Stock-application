from django.conf import settings
from payment.models import Payment, Buy, Sell
from .models import Profile, price_db
from django.db.models import Sum


class WalletTransaction():
    def __init__(self, balance, stock_eq):
        self.balance = balance
        self.stock_eq = stock_eq
        
    def stock_eq_update(self, total_selling_amount):
        self.stock_eq -= total_selling_amount
        return self.stock_eq    
    
    def balance_update(self, total_selling_amount):
        self.balance += total_selling_amount
        return self.balance 
 
    
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
        bal = self.balance
        return bal
    
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
        
    def get_balance(self):              #This function returns the account balance 
        return self.balance
    
    
    def sell(self, shares, stock_shares):              #This function is run when the user wants to sell a stock
        if shares <= stock_shares:
            stock_shares -= shares
            return stock_shares
        else:     
            print("You dont have that amount of money in shares")
            return False