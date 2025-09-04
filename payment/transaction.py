from dataclasses import dataclass, field

@dataclass 
class WalletTransaction:
    __slots__ = ("balance", "stock_eq")  
    balance: float
    stock_eq: float
        
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
 

@dataclass
class StockHolding(WalletTransaction):
    __slots__ = ("balance", "stock_eq")  # Extends parent slots
    def __init__(self, balance, stock_eq):
        super().__init__(balance, stock_eq, )
    
    
    def buy_shares(self, shares1, shares):                  #This function updates the number of shares after a buy transaction
        shares1 += shares 
        return shares1
    
    def sell_shares(self, shares1, shares):                 #This function updates the number of shares after a sell transaction
        shares -= shares1 
        return shares
     

@dataclass   
class BuyTransaction:
    __slots__ = ("balance", "shares")  
    balance : float
    shares : float

        
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
  
  
@dataclass               
class SellTransaction:
    __slots__ = ("_balance", "_shares")  # Private slot names
    balance: float 
    shares: float 


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
        
@dataclass      
class Trading:
    __slots__ = ("_balance", "_leverage")  
    _balance : float
    _leverage : int
      
        
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
    
    
"""

balance = float(10000)
stock_eq = float(0.0)


leverage = int(3)
amount = float(100)
current_price = float(120.00)
long_price = float(100.00)
short_price = float(100.00)


Transaction_instance = SellTransaction(balance, leverage)

#Transaction_instance.buy_balance_update(100)
#Transaction_instance.buy_stock_eq_update(100)


#Transaction_instance.long_position(amount, long_price, current_price)
#Transaction_instance.short_position(amount, short_price, current_price)

#print(Transaction_instance.balance, Transaction_instance.stock_eq)
"""