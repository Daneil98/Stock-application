from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('deposit_list/', views.PaymentListView.as_view(), name='deposit_list'),
    path('deposit/', views.Payment.as_view(), name='deposit'),
    
    path('wallet/', views.WalletListView.as_view(), name='wallet_view'),
    path('wallet/<pk>/', views.WalletDetailView.as_view(), name='wallet_detail'),
    

    path('buy/', views.BuyView.as_view(), name='buy'),
    path('buy_stock/', views.BuyUpdate.as_view(), name='buy_stock'),

    path('sell/', views.SellDetailView.as_view(), name='sell'),
    path('sell_stock/', views.SellUpdate.as_view(), name='sell_stock'),
    
    path('stock_wallet/', views.StockWalletView.as_view(), name='stockwallet_view'),
    path('stock_wallet_update/', views.StockWalletUpdate.as_view(), name='stock_wallet_update'),
    
    path('amount/<pk>/', views.AmountView.as_view(), name='amount'),
]
