from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from .models import pokedexUser


# Password reset form which validates that an
# account exists for the given email
class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


# User can update and add extra profile information
class PokedexUserUpdateForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'website_url', 'bio', 'go_trainer_id', 'trainer_qr_code', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(PokedexUserUpdateForm, self).__init__(*args, **kwargs)
        for fieldname in ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'website_url', 'bio', 'go_trainer_id', 'trainer_qr_code', 'profile_picture']:
            self.fields[fieldname].widget.attrs = {'class': 'form-control'}


# User can update email address or password
# Validate password against password validators
class AccountForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Old Password'}
        ), label="Old Password")
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'New Password'}
        ), label="New Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm New Password'}
        ), label="Confirm New Password")

    class Meta:
        model = pokedexUser
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter your email here'}),
        }

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password(new_password, self.instance)
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password',
                           "New password and confirm password do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
