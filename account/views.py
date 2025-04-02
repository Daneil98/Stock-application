from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from .models import Profile, price_db
from .forms import *
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
@csrf_protect  # Prefer this over csrf_exempt
def ticker(request):
    if request.method != 'POST':
        return redirect('account:stocks')  # Or handle GET requests differently
    
    ticker_symbol = request.POST.get('ticker')
    if not ticker_symbol:
        messages.error(request, "No ticker symbol provided.")
        return redirect('account:stocks')
    
    try:
        # Fetch data (add error handling for external API failures)
        price_data = get_price(ticker_symbol)
        meta_data = get_meta_data(ticker_symbol)
        
        # Validate required keys exist
        close_price = price_data.get('close')
        open_price = price_data.get('open')
        stock_name = meta_data.get('name')
        
        if None in (close_price, open_price, stock_name):
            raise ValueError("Missing required data fields")
        
        # Save to database
        price_db.objects.create(
            user=request.user.username,
            closeprice=close_price,
            openprice=open_price,
            name=stock_name,
            ticker=ticker_symbol
        )
        
        return render(request, 'account/ticker.html', {
            'ticker': ticker_symbol,
            'meta': meta_data,
            'price': price_data
        })
    
    except Exception as e:
        messages.error(request, f"Error processing ticker: {str(e)}")
        return redirect('account:stocks')



#BLOG VIEW
def post_list(request, tag_slug=None):
    return render(request, 'blog/post_list.html', {'section': 'post_list'})
