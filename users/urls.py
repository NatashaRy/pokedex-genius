from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('signup/', views.signup_view, name='account_signup'),
    path('login/', views.login_view, name='account_login'),
]
