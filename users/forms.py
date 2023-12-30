from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import pokedexUser


class CustomPasswordResetForm(PasswordResetForm):
    """
    Validates that an account exists for the given email address
    """
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    class Meta:
        model = pokedexUser
        fields = ['date_of_birth', 'website_url', 'bio', 'go_trainer_id',
                  'first_name', 'last_name', 'username',
                  'trainer_qr_code', 'profile_picture', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'height': '100px'}),
            'go_trainer_id': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer_qr_code': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
