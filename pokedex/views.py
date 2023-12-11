from django.shortcuts import render
from django.views import generic
from .models import Pokedex


def dashboard(request):
    """
    Render the dashboard.html template
    """
    return render(request, 'pokedex/dashboard.html')


class PokedexList(generic.ListView):
    model = Pokedex
    queryset = Pokedex.objects.filter(status=1).order_by('-created_on')
    template_name = 'pokedex/dashboard.html'
    paginate_by = 9
