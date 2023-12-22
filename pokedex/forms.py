from django import forms
from .models import UserPokemon, Pokedex


# Dropdown with Pokemon on search.html
class PokemonDropdown(forms.Form):
    def __init__(self, choices=None, *args, **kwargs):
        super(PokemonDropdown, self).__init__(*args, **kwargs)
        self.fields['pokemon'] = forms.ChoiceField(choices=choices or [])


# Form to add Pokemon to Pokedex
class AddUserPokemonForm(forms.ModelForm):
    entry_number = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddUserPokemonForm, self).__init__(*args, **kwargs)
        self.fields['pokedex'].choices = [
            ('', 'Select Pokedex to add Pokemon to')
            ] + list(self.fields['pokedex'].choices)[1:]

    class Meta:
        model = UserPokemon
        exclude = ['user', 'pokemon_id']

    def clean(self):
        cleaned_data = super().clean()
        pokedex_user = self.user
        selected_pokemon_id = cleaned_data.get('entry_number')
        selected_pokedex_id = cleaned_data.get('pokedex')

        if UserPokemon.objects.filter(
            user=pokedex_user,
            pokemon_id=selected_pokemon_id,
            pokedex=selected_pokedex_id
        ).exists():
            raise forms.ValidationError(
                'You already have this pokemon in your pokedex!')

        return cleaned_data

    def save(self, commit=True):
        instance = super(AddUserPokemonForm, self).save(commit=False)
        instance.pokemon_id = self.cleaned_data.get('entry_number')
        instance.pokemon_name = self.cleaned_data.get('pokemon_name')
        if commit:
            instance.save()
        return instance


# Form to customize Pokedex when creating
class PokedexForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'color', 'class': 'form-control form-control-color'}
        )
    )

    class Meta:
        model = Pokedex
        fields = ['name', 'description', 'cover_image', 'color', 'is_favorite']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': ' '}
                ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': ' '}
                ),
            'is_favorite': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
                ),
        }
