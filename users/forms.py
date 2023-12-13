from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import pokedexUser


class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        """
        Validates that an account exists for the given email.
        """
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


class UpdateProfilePicture(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ('profile_picture',)


class BioForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ('bio',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ('username', 'website_url', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''


class TrainerForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ('go_trainer_id', 'trainer_qr_code')


class AccountForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(), label="Old Password")
    new_password = forms.CharField(
        widget=forms.PasswordInput(), label="New Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm New Password")

    class Meta:
        model = pokedexUser
        fields = ('email',)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password',
                           "New password and confirm new password do not match"
                           )

        if old_password and not self.instance.check_password(old_password):
            self.add_error('old_password', "Old password is not correct")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
