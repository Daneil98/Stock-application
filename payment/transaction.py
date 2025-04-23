
class WalletTransaction():
    def __init__(self, balance, stock_eq):
        self.balance = balance
        self.stock_eq = stock_eq
        
    def buy_stock_eq_update(self, totalamount):                     #This function updates the stock equities after a buy transaction
        self.stock_eq += totalamount
        return self.stock_eq   
     
    def sell_stock_eq_update(self, totalamount):                    #This function updates the stock equities after a sell transaction
        self.stock_eq -= totalamount
        return self.stock_eq    
    
    def buy_balance_update(self, totalamount):                      #This function updates the user's account balance after a buy transaction
        self.balance -= totalamount
        return self.balance 
    
    def sell_balance_update(self, totalamount):                     #This function updates the user's account after a sell transaction
        self.balance += totalamount
        return self.balance 
 
 
class StockHolding(WalletTransaction):
    def __init__(self, balance, stock_eq):
        super().__init__(balance, stock_eq, )
    
    
    def buy_shares(self, shares1, shares):                  #This function updates the number of shares after a buy transaction
        shares1 += shares 
        return shares1
    
    def sell_shares(self, shares1, shares):                 #This function updates the number of shares after a sell transaction
        shares -= shares1 
        return shares
     
    
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
    
    def share_number(self, sell_amount, price):                  #This function calculates the number of shares to be sold
        numbers = sell_amount / price
        
        if numbers < 0:
            print("Not Possible")
        else:
            return numbers
    
    def sell(self, sell_amount, eq):              #This function is run when the user wants to sell a stock
        if sell_amount > eq:
            print("You dont have that amount of money in equity")
            return False
        else:     
            eq -= sell_amount
            return eq
        
        
class Trading():
    def __init__(self, balance, leverage):
        self._balance = balance
        self._leverage = leverage
      
        
    def long_position(self, amount, long_price, current_price):
        if long_price <= 0 or current_price <= 0:
            raise ValueError("Prices must be positive and greater than zero.")
    
        if amount <= 0:
            raise ValueError("Amount must be positive and greater than zero.")
        
        spread = (current_price - long_price) / current_price                         #When going long, we make profit when the current price is greater than the long price
        returns = spread * self._leverage * amount
        return returns
        
    
    def short_position(self, amount, short_price, current_price):
        if short_price <= 0 or current_price <= 0:
            raise ValueError("Prices must be positive and greater than zero.")
    
        if amount <= 0:
            raise ValueError("Amount must be positive and greater than zero.")
        
        spread = (short_price - current_price) / short_price                   #When going short, we make profit when the current price is less than the short price
        returns = spread * self._leverage * amount
        return returns    
        
    def close_position(self, returns):
        self._balance += returns
        return self._balance
    
