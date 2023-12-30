from django import forms
from .models import UserPokemon, Pokedex


class PokemonDropdown(forms.Form):
    """
    Dropdown with list of Pokemon from the PokeAPI
    """
    def __init__(self, choices=None, *args, **kwargs):
        super(PokemonDropdown, self).__init__(*args, **kwargs)
        self.fields['pokemon'] = forms.ChoiceField(
            choices=choices or [],
            widget=forms.Select(attrs={'class': 'form-select'})
        )


class AddUserPokemonForm(forms.ModelForm):
    """
    Form to add Pokemon to Pokedex. Holdes the Pokemons entry number and
    validates that the user does not already exist in the user's Pokedex.
    A save method is also defined to save the Pokemon to the user's Pokedex.
    """
    entry_number = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddUserPokemonForm, self).__init__(*args, **kwargs)
        self.fields['pokedex'].choices = [
            ('', 'Select Pokedex to add Pokemon to')
            ] + list(self.fields['pokedex'].choices)[1:]
        self.fields['pokemon_name'].required = False

    class Meta:
        model = UserPokemon
        exclude = ['user', 'pokemon_id']

    def clean(self):
        cleaned_data = super().clean()
        pokedex_user = self.user
        selected_pokemon_id = cleaned_data.get('entry_number')
        selected_pokedex_id = cleaned_data.get('pokedex')

        if not selected_pokedex_id:
            raise forms.ValidationError(
                'Please select a Pokedex to add this Pokemon to.')

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


class PokedexForm(forms.ModelForm):
    """
    Form for create or update a Pokedex
    """
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
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control-file'}),
        }
