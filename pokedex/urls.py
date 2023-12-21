from django.urls import path
from . import views
from .views import PokedexCreateView, PokedexDetailsView, PokedexUpdateView, PokedexDeleteView

urlpatterns = [
     path('dashboard/', views.dashboard, name='dashboard'),

     path('search/', views.search, name='search'),

     path('pokemon/<int:entry_number>/',
          views.pokemon_details,
          name='pokemon_details'),

     path('pokedex/create/',
          PokedexCreateView.as_view(),
          name='pokedex_create'),

     path('pokedex/<slug:slug>/',
          PokedexDetailsView.as_view(),
          name='pokedex_details'),

     path('pokedex/<slug:slug>/update/',
          PokedexUpdateView.as_view(),
          name='pokedex_update'),

     path('pokedex/<slug:slug>/delete/',
          PokedexDeleteView.as_view(),
          name='pokedex_delete'),
]
