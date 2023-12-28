from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import (CustomPasswordResetForm, PokedexUserUpdateForm)


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

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        bio = request.POST.get('bio', '')
        website_url = request.POST.get('website_url', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        go_trainer_id = request.POST.get('go_trainer_id', '')

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.email = email
        user_profile.bio = bio
        user_profile.website_url = website_url
        user_profile.date_of_birth = date_of_birth
        user_profile.go_trainer_id = go_trainer_id

        # Handling file uploads
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture

        trainer_qr_code = request.FILES.get('trainer_qr_code')
        if trainer_qr_code:
            user_profile.trainer_qr_code = trainer_qr_code

        user_profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request,
                  'users/update_profile.html', {'user_profile': user_profile})
