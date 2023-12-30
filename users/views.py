from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import (CustomPasswordResetForm, CustomPasswordChangeForm,
                    UserProfileForm)
from django.contrib.auth import logout


def login_view(request):
    """
    View for user login
    """
    return render(request, 'login.html')


def signup_view(request):
    """
    View for user signup
    """
    return render(request, 'signup.html')


@login_required
def profile_view(request):
    """
    View for user profile, user must be logged in
    """
    form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


@login_required
def update_profile(request):
    """
    View for updating user profile, user must be logged in
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'form': form})


def change_password(request):
    """
    View for changing password, user must be logged in
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your password has been successfully updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Could not update password.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'update_profile.html',
                  {'password_change_form': form})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


@login_required
def delete_account(request):
    """
    View for deleting account, user must be logged in
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request,
                         'Your account has been successfully deleted.')
        return redirect('index')
    else:
        return render(request, 'confirm_delete.html')
