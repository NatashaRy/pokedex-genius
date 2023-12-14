from django.urls import path
from . import views
from .views import search

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('search/', search, name='search'),
]
