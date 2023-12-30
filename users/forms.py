from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
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


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Customized PasswordChangeForm
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'placeholder': 'Old Password',
            'class': 'form-control floating-label',
        })

        self.fields['new_password1'].widget.attrs.update({
            'placeholder': 'New Password',
            'class': 'form-control floating-label',
        })

        self.fields['new_password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control floating-label',
        })

        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm Password'


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    class Meta:
        model = pokedexUser
        fields = ['date_of_birth', 'website_url', 'bio', 'go_trainer_id',
                  'trainer_qr_code', 'profile_picture']

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
        'website_url': forms.URLInput(attrs={'class': 'form-control'}),
        'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'go_trainer_id': forms.TextInput(attrs={'class': 'form-control'}),
        'trainer_qr_code': forms.ClearableFileInput(
            attrs={'class': 'form-control-file'}),
        'profile_picture': forms.ClearableFileInput(
            attrs={'class': 'form-control-file'}),
    }

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=False)
    date_of_birth = forms.DateField(required=False)
    website_url = forms.URLField(required=False)
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'height': '100px'}), required=False)
    go_trainer_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    trainer_qr_code = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        required=False)
    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        required=False)
