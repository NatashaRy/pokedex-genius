from django import forms
from datetime import datetime


class PokemonDropdown(forms.Form):
    def __init__(self, choices=None, *args, **kwargs):
        super(PokemonDropdown, self).__init__(*args, **kwargs)
        self.fields['pokemon'] = forms.ChoiceField(choices=choices or [])


class AddPokemonForm(forms.Form):
    pokedex_id = forms.IntegerField()
    date_added = forms.DateTimeField(
        initial=datetime.now(),
        widget=forms.HiddenInput()
        )
    additional_notes = forms.CharField(
        max_length=200,
        widget=forms.Textarea, required=False
        )

    class Meta:
        fields = ('pokedex_id',
                  'date_added'
                  'additional_notes')
