from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from .forms import (CustomPasswordResetForm, UpdateProfilePicture,
                    BioForm, ProfileForm, TrainerForm, AccountForm)
from .models import pokedexUser


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')


@login_required
def profile_view(request):
    user_profile = pokedexUser.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'user_profile': user_profile})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


# Instansiate forms with POST data,
# Checks which button was clicked and validates the corresponding form
@login_required
def update_profile(request):
    user_profile = pokedexUser.objects.get(user=request.user)

    if request.method == 'POST':
        picture_form = UpdateProfilePicture(request.POST, request.FILES, instance=user_profile, prefix='pic')
        bio_form = BioForm(request.POST, instance=user_profile, prefix='bio')
        profile_form = ProfileForm(request.POST, instance=user_profile, prefix='profile')
        trainer_form = TrainerForm(request.POST, request.FILES, instance=user_profile, prefix='trainer')
        account_form = AccountForm(request.POST, instance=user_profile, prefix='account')

        if 'update_picture' in request.POST and picture_form.is_valid():
            picture_form.save()
        elif 'update_bio' in request.POST and bio_form.is_valid():
            bio_form.save()
        elif 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
        elif 'update_trainer' in request.POST and trainer_form.is_valid():
            trainer_form.save()
        elif 'update_account' in request.POST and account_form.is_valid():
            account_form.save()
            return redirect('profile')
    else:
        picture_form = UpdateProfilePicture(instance=user_profile, prefix='pic')
        bio_form = BioForm(instance=user_profile, prefix='bio')
        profile_form = ProfileForm(instance=user_profile, prefix='profile')
        trainer_form = TrainerForm(instance=user_profile, prefix='trainer')
        account_form = AccountForm(instance=user_profile, prefix='account')

    context = {
        'picture_form': picture_form,
        'bio_form': bio_form,
        'profile_form': profile_form,
        'trainer_form': trainer_form,
        'account_form': account_form
    }
    return render(request, 'users/update_profile.html', context)
