from django.urls import path, include


from . import views

app_name = 'payment'


urlpatterns = [
# ... 
    path('process/', views.payment_process, name='process'), 
    path('done/', views.payment_done, name='done'), 
    path('canceled/', views.payment_canceled, name='canceled'),
    path('stock_buy/', views.stock_buy, name='stock_buy'),
    path('stock_sell/', views.stock_sell, name='stock_sell'), 
]