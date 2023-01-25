from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, TickerForm, FAQForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from .tiingo import get_meta_data, get_price
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from blog.views import post_list
from blog.models import Post, Comment
from blog.forms import EmailPostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
# Create your views here.


def about(request):
    form = FAQForm(request.POST)
    return render(request, 'about.html', {'form': form})    

def base(request):
    return render(request, 'base.html')    

def index(request):
    return render(request, 'index.html')   



#ACCOUNT FUNCTIONS
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
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
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
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})




#STOCK FUNCTIONS
def stock(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect('ticker/')
    else:
        form = TickerForm()
    return render(request, 'account/stock.html', {'form': form})


def ticker(request, **ticker):
    ticker = request.POST['ticker']
    return render(request, 'account/ticker.html', {'ticker': ticker, 'meta': get_meta_data(ticker), 'price': get_price(ticker)})




def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    posts = Post.published.order_by()
    object_list = Post.published.order_by()
    paginator = Paginator(object_list, 2) # 2 posts in each page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        page_obj= paginator.get_page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'posts': posts, 'tag': tag})