from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Profile, price_db
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, TickerForm, FAQForm
from django.contrib import messages
from django.shortcuts import render
from .tiingo import get_meta_data, get_price
from django.shortcuts import render
from payment.models import Wallet, Payment, Stock_Wallet
import pyotp


# Create your views here.



#BASIC VIEWS
@login_required
def about(request):
    form = FAQForm(request.POST)
    return render(request, 'about.html', {'form': form, 'section': 'about'})    

def base(request):
    return render(request, 'base.html')    
   

def index(request):
    return render(request, 'index.html')   

#ACCOUNT VIEWS
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'account/dashboard.html')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    
    total_amount = Payment.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum']
    total = f"{float(total_amount):.2f}"
    recent = Wallet.objects.order_by('-id').first()
    
    if recent:
        equity = f"{float(recent.stock_eq):.2f}"
        balance = f"{float(recent.balance):.2f}"
        
    else:
        equity = 0
        balance = 0
    
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'total': total, 'equity': equity, 'balance': balance})

def my_stocks(request):
    stocks_owned = Stock_Wallet.objects.order_by('-id').all()
    assets_dict = {}

    for stock in stocks_owned:
        if stock.name not in assets_dict:
            assets_dict[stock.name] = {
                'equity': f"{float(stock.equity):.2f}",
                'shares': f"{float(stock.shares):.2f}"
            }

    assets = [{'stock_name': name, 'equity': data['equity'], 'shares': data['shares']} for name, data in assets_dict.items()]
    return render(request, 'account/my_stocks.html', {'section': 'my_stocks', 'assets': assets})


def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):

    secret = pyotp.random_base32()
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'section': 'edit', 'secret': secret})




#STOCK VIEWS
@login_required
def stock(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker', None]
            return HttpResponseRedirect('<ticker>/')
    else:
        form = TickerForm()
    return render(request, 'account/stock.html', {'form': form})


@login_required
@csrf_exempt
def ticker(request, **ticker):  
    ticker = request.POST['ticker']
    stock_instance = price_db()                     #Create a stock instance for the price_db model
    prize = {'type': get_price(ticker)}
    price = (prize["type"])                         #Sets price as a dictionary with prize and type as key-value pair
    close_price = price['close']                    # Extracts the "close" value
    open_price = price['open']                      # Extracts the "open" value
    
    name = {'typ': get_meta_data(ticker)}
    meta = (name['typ'])
    stock_name = meta['name']
    
    user = request.user                     #Request user
    stock_instance.user = user.username
    stock_instance.closeprice = close_price
    stock_instance.openprice = open_price
    stock_instance.name = stock_name
    stock_instance.save()
    
    return render(request, 'account/ticker.html', {'ticker': ticker, 'meta': get_meta_data(ticker), 'price': get_price(ticker)})



#BLOG VIEW
def post_list(request, tag_slug=None):
    return render(request, 'blog/post_list.html', {'section': 'post_list'})
