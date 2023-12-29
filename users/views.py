from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import (CustomPasswordResetForm, ProfileUpdateForm)
from django.contrib.auth import logout


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html',
                  {'user_profile': request.user})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


@login_required
def update_profile(request):
    """
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request,
                         'Your account has been successfully deleted.')
        return redirect('index')
    else:
        return render(request, 'confirm_delete.html')
