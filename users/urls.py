from django.urls import path
from . import views
from .views import CustomPasswordResetView, update_profile, profile_view

urlpatterns = [
    path('signup/', views.signup_view, name='account_signup'),
    path('login/', views.login_view, name='account_login'),
    path('password_reset/',
         CustomPasswordResetView.as_view(),
         name='accounts_password_reset'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/', profile_view, name='profile'),
]
