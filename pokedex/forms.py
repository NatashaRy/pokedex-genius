from django import forms


class PokemonDropdown(forms.Form):
    def __init__(self, choices=None, *args, **kwargs):
        super(PokemonDropdown, self).__init__(*args, **kwargs)
        self.fields['pokemon'] = forms.ChoiceField(choices=choices or [])
