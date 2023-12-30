from django.urls import path
from . import views
from .views import CustomPasswordResetView, update_profile, account_view

urlpatterns = [
    path('signup/', views.signup_view, name='account_signup'),
    path('login/', views.login_view, name='account_login'),
    path('password/reset/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('account/', account_view, name='account'),
    path('account/settings/', update_profile, name='account_settings'),
]
