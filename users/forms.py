from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from .models import pokedexUser
from datetime import date
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CustomPasswordResetForm(PasswordResetForm):
    """
    Validates that an account exists for the given email address
    """
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ['username', 'password', 'date_of_birth',
                  'website_url', 'bio', 'go_trainer_id']
        widgets = {
            'password': forms.PasswordInput(),
        }


class AccountForm(forms.ModelForm):
    """
    Account form for updating email address
    """
    class Meta:
        model = pokedexUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Enter your email here'})

        self.fields['email'].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField('email', placeholder="Email")
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if pokedexUser.objects.filter(
            email=email
            ).exclude(
                pk=self.instance.pk
                ).exists():
            raise ValidationError(
                "This email address is already in use. Please choose another.")
        return email


class PasswordChangeForm(forms.Form):
    """
    Form to change password
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}),
        label="Old password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm New Password'}),
        label="Confirm Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control'})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField('old_password',
                          placeholder="Old Password"),
            FloatingField('new_password',
                          placeholder="New Password"),
            FloatingField('confirm_password',
                          placeholder="Confirm New Password"),
        )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise ValidationError("Your old password was entered incorrectly. "
                                  "Please enter it again.")
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        password_validation.validate_password(new_password, self.instance)
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password',
                           "New password and confirm new password "
                           "do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
