from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import PokedexCreateView, PokedexDetailsView, PokedexUpdateView, PokedexDeleteView, PokemonDeleteView

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

     path('pokedex/<slug:pokedex_slug>/delete-pokemon/<int:pokemon_id>/',
          PokemonDeleteView.as_view(),
          name='pokemon_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
