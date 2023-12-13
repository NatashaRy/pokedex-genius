from django import forms


class PokemonSearchForm(forms.Form):
    query = forms.CharField(label='Search for a Pokemon')
