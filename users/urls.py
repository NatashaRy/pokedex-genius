from django.urls import path
from . import views
from .views import (CustomPasswordResetView, profile_view)

urlpatterns = [
    path('signup/', views.signup_view, name='account_signup'),
    path('login/', views.login_view, name='account_login'),
    path('password/reset/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
