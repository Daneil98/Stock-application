from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api'


urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),        #Good
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       #Good
    
    path('login/', views.LoginView.as_view(), name='login'),                        #Good
    path('register/', views.RegisterView.as_view(), name='register'),               #Good
    
    
    path('deposit_list/', views.PaymentListView.as_view(), name='deposit_list'),    #Good
    path('deposit/', views.Deposit.as_view(), name='deposit'),                      #Good
    
    
    path('ticker/', views.Ticker.as_view(), name='ticker'),                         #Good
    path('my_stocks/', views.MyStocks.as_view(), name='my_stocks'),                 #Good
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),                #Good
    path('edit/', views.Edit.as_view(), name='edit'),                               #Good
    
    path('stock_buy/', views.StockBuy.as_view(), name='stock_buy'),                 #Good
    path('stock_buys/', views.BuyView.as_view(), name='stock_buys'),                #Good
    
    path('stock_sell/', views.StockSell.as_view(), name='stock_sell'),              #Good
    path('stock_sells/', views.SellListView.as_view(), name='stock_sells'),         #Good
    
    
    path('amount/', views.AmountView.as_view(), name='amount'),                     #Good
    

    path('long/', views.LongPosition.as_view(), name='long'),                       #Good
    path('short/', views.ShortPosition.as_view(), name='short'),                    #Good

]
