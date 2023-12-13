from django.urls import path
from . import views
from .views import search_pokemon

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('search/', search_pokemon, name='search_pokemon'),
    path('pokemon/<str:pokemon_name>/', views.pokemon_detail, name='pokemon_detail'),
]
