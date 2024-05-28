from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logged_out/', auth_views.LogoutView.as_view(), name='logged_out'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('about/', views.about, name='about'),
    path('post_list/', views.post_list, name='post_list'),
    path('ticker/', views.ticker, name='ticker'),
    path('post_list/', views.post_list, name='post_list'),
    path('stocks/', views.stock, name='stocks'),
    path('my_stocks/', views.my_stocks, name='my_stocks')
]
