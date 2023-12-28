from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import (CustomPasswordResetForm, PokedexUserUpdateForm, AccountForm)
from django.contrib.auth import logout


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user_profile': request.user})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


# Instansiate forms with POST data,
# Checks which button was clicked and validates the corresponding form
@login_required
def update_profile(request):
    user_profile = request.user
    user_form = PokedexUserUpdateForm(instance=user_profile)
    account_form = AccountForm(instance=user_profile)
    if user_form.is_valid() and account_form.is_valid():

        if request.method == 'POST':
            user_form = PokedexUserUpdateForm(request.POST, request.FILES, instance=user_profile)
            account_form = AccountForm(request.POST, instance=user_profile)

            if user_form.is_valid() and account_form.is_valid():
                user_form.save()
                account_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the error below.")

    return render(request, 'users/update_profile.html', {
        'user_form': user_form,
        'account_form': account_form,
        'user_profile': user_profile
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('index')
    else:
        return render(request, 'confirm_delete.html')
