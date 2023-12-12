from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from crispy_forms.bootstrap import PrependedText, FormActions
from .models import CustomUser


class CustomSignupForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    accept_terms = forms.BooleanField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'accept_terms'
        )

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username',
                  css_class='form-control',
                  placeholder='Username'),
            Field('email',
                  css_class='form-control',
                  placeholder='Email'),
            Field('password1',
                  css_class='form-control',
                  placeholder='Password'),
            Field('password2',
                  css_class='form-control',
                  placeholder='Repeat Password'),
            Field('accept_terms',
                  css_class='form-check-input'),
            Submit('submit',
                   'Sign up',
                   css_class='btn btn-primary')
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('login',
                  css_class='form-control',
                  placeholder='Username or Email'),
            Field('password',
                  css_class='form-control',
                  placeholder='Password'),
            Div(
                PrependedText('remember', ''),
                css_class='form-check'
            ),
            FormActions(
                Submit('submit', 'Log in', css_class='btn btn-primary'),
                Div(css_class='forgot-password')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
