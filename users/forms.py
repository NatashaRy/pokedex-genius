from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm,
    AuthenticationForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import pokedexUser

User = get_user_model()

# ============================================================
# LOGIN/SIGNUP/LOGOUT
# ============================================================

class CustomSignupForm(UserCreationForm):
    """
    Custom signup form
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    
    class Meta:
        model = pokedexUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with remember me field
    """
    remember = forms.BooleanField(
        required=False,
        initial=False,
        label='Remember me'
    )


# ============================================================
# PASSWORD
# ============================================================

class CustomPasswordResetForm(PasswordResetForm):
    """
    Validates that an account exists for the given email address
    """
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


# ============================================================
# ACCOUNT
# ============================================================

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    class Meta:
        model = pokedexUser
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'website_url', 'bio', 'go_trainer_id'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'height': '100px'}),
            'go_trainer_id': forms.TextInput(attrs={'class': 'form-control'}),
        }