from django.urls import path
from . import views
from .views import search, pokemon_details

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('search/', search, name='search'),
    path('pokemon/<int:entry_number>/',
         pokemon_details, name='pokemon_details'
         )
]
