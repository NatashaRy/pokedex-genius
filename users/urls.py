from django.urls import path, reverse_lazy
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordChangeView,
    update_profile,
    account_view,
    )
from django.contrib.auth import views as auth_views


urlpatterns = [
    # ============================================================
    # LOGIN/SIGNUP/LOGOUT
    # ============================================================

    path('signup/', views.signup_view, name='custom_signup'),
    path('login/', views.login_view, name='custom_login'),
    path('logout/', views.logout_view, name='custom_logout'),

    # ============================================================
    # PASSWORD
    # ============================================================

    # 1. Request password reset
    path('reset-password/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),
    
    # 2. Confirmation that email has been sent
    path('reset-password/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    # 3. Link from email (with uid and token)
    path('reset-password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    
    # 4. Confirmation that password is changed
    path('reset-password/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('account/change-password/',
         CustomPasswordChangeView.as_view(),
         name='password_change'),

    # ============================================================
    # ACCOUNT
    # ============================================================

    path('delete-account/', views.delete_account, name='delete_account'),
    path('account/', account_view, name='account'),
    path('account/settings/', update_profile, name='update_profile'),
]
