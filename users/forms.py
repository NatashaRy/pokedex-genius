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
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 200px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(BioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.bio:
            self.fields['bio'].widget.attrs['placeholder'] = self.instance.bio


class ProfileForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ('username',
                  'first_name',
                  'last_name',
                  'website_url',
                  'date_of_birth')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username here'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name here'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name here'
            }),
            'website_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your website url here'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your date of birth here'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''


class TrainerForm(forms.ModelForm):
    class Meta:
        model = pokedexUser
        fields = ('go_trainer_id', 'trainer_qr_code')
        widgets = {
            'go_trainer_id': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter your trainer id here'}),
        }


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
