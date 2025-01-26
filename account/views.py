from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Profile, price_db
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, TickerForm, FAQForm
from django.contrib import messages
from .tiingo import get_meta_data, get_price
from payment.models import Wallet, Payment, Stock_Wallet, Long, Short
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
    
    name = request.user.username
    total_amount = Payment.objects.filter(user=name, paid=True).last()
    
    recent = Wallet.objects.filter(user=name).last()
    
    if recent and total_amount:
        equity = f"{float(recent.stock_eq):.2f}"
        balance = f"{float(recent.balance):.2f}"
        total = f"{float(total_amount.amount):.2f}"
        
    else:
        equity = 0
        balance = 0
        total = 0
    
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'total': total, 'equity': equity, 'balance': balance})


@login_required
def my_stocks(request):
    name = request.user.username
    
    stocks_owned = Stock_Wallet.objects.filter(user=name).all()
    
    long_trades = Long.objects.filter(user=name).all()
    short_trades = Short.objects.filter(user=name).all()
    
    if not long_trades.exists() and not short_trades.exists():
        # Handle case where there are no trades
        context = {'message': 'No trades available for this user.', 'long_trades': None, 'short_trades': None}
    
    else:
        context = {'long_trades': long_trades, 'short_trades': short_trades}
    
    if not stocks_owned.exists():
        # Handle case where there are no trades
        assets = {'message': 'No trades available for this user.', 'stocks_owned': None}
    
    else:
        assets = {'stocks_owned': stocks_owned,}
    return render(request, 'account/my_stocks.html', {'assets': assets, 'context': context})


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
    prize = {'type': get_price(ticker)}
    price = (prize["type"])                         #Sets price as a dictionary with prize and type as key-value pair
    close_price = price['close']                    # Extracts the "close" value
    open_price = price['open']                      # Extracts the "open" value
    
    name = {'typ': get_meta_data(ticker)}
    meta = (name['typ'])
    stock_name = meta['name']
    
    user_name = request.user.username                     #Request user
    price_db.objects.create(user = user_name, closeprice = close_price, 
        openprice = open_price, name = stock_name, ticker = ticker)
    
    return render(request, 'account/ticker.html', {'ticker': ticker, 'meta': get_meta_data(ticker), 'price': get_price(ticker)})



#BLOG VIEW
def post_list(request, tag_slug=None):
    return render(request, 'blog/post_list.html', {'section': 'post_list'})
