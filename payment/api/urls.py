from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payment_view'),
    path('payment/<pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    
    path('wallet/', views.WalletListView.as_view(), name='wallet_view'),
    path('wallet/<pk>/', views.WalletDetailView.as_view(), name='wallet_detail'),
    
    path('buy/', views.BuyListView.as_view(), name='Buy_view'),
    path('buy/<pk>/', views.BuyDetailView.as_view(), name='Buy_detail'),
    #path('buy/<pk>/Buy', views.BuyUpdate.as_view(), name='Buy_update'),

    path('sell/', views.SellListView.as_view(), name='sell_view'),
    path('sell/<pk>/', views.SellDetailView.as_view(), name='sell_detail'),
    #path('sell/<pk>/Sell', views.SellUpdate.as_view(), name='Sell_update'),
    
    path('amount/', views.AmountListView.as_view(), name='amount_view'),
    path('amount/<pk>/', views.AmountDetailView.as_view(), name='amount_detail'),
]
