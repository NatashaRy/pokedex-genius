from django import forms
from .models import UserPokemon, Pokedex


class PokemonDropdown(forms.Form):
    def __init__(self, choices=None, *args, **kwargs):
        super(PokemonDropdown, self).__init__(*args, **kwargs)
        self.fields['pokemon'] = forms.ChoiceField(choices=choices or [])


class AddUserPokemonForm(forms.ModelForm):
    class Meta:
        model = UserPokemon
        fields = ('pokemon_id',
                  'pokedex',
                  )
        widgets = {
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pokedexUser = self.user
        selected_pokemon_id = cleaned_data.get('pokemon_id')
        selected_pokedex_id = cleaned_data.get('pokedex')

        if UserPokemon.objects.filter(
            user=pokedexUser,
            pokemon_id=selected_pokemon_id,
            pokedex=selected_pokedex_id
        ).exists():
            raise forms.ValidationError(
                'You already have this pokemon in your pokedex!')

        # if not PokedexList.objects.filter(user=user, id=selected_pokedex_id).exists():
        #     raise forms.ValidationError(
        #         'You do not own the selected Pokedex!'
        #         'Please select an other Pokedex.'
        #         )

        return cleaned_data


class PokedexForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'color', 'class': 'form-control'}))

    class Meta:
        model = Pokedex
        fields = ['name',
                  'description',
                  'cover_image',
                  'color',
                  'is_public',
                  'is_favorite',
                  ]
