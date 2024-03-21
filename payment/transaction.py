
class WalletTransaction():
    def __init__(self, balance, stock_eq):
        self.balance = balance
        self.stock_eq = stock_eq
        
    def stock_eq_update(self, totalamount): 
        self.stock_eq -= totalamount
        return self.stock_eq    
    
    def buy_balance_update(self, totalamount):
        self.balance -= totalamount
        return self.balance 
    
    def sell_balance_update(self, totalamount):
        self.balance += totalamount
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
    
    def share_number(self, sell_amount, price):                  #This function calculates the number of shares bought
        numbers = sell_amount / price
        self.shares -= numbers
        shares = self.shares
        return shares
    
    def sell(self, sell_amount, eq):              #This function is run when the user wants to sell a stock
        if sell_amount <= eq:
            eq -= sell_amount
            return eq
        else:     
            print("You dont have that amount of money in equity")
            return False