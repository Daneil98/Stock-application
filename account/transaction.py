from django.conf import settings
from payment.models import Payment
from .models import Profile


class Transaction(object):
    def __init__(self, request):
        self.session = request.session
        transaction = self.session.get(settings.TRANSACTION_SESSION_ID)
        
    def get_account(self, account):
        return self.account
    
    def deposit(self, amount):
        self.balance += amount
        
    def get_balance(self):
        return self.balance
    
    def charge(self, price):
        if price > self.balance:
            return False
        else:
            self.balance -= price
            return True
        
    def sell(self, price):
        self.balance += price
        

if __name__=="__main__":
    payment = Payment.objects.get(all)
    subtotal = sum(payment.amount)
    _user = Profile.user
    result = Transaction()
    result.deposit(subtotal)
    result.account(_user)
    