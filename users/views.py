from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from .forms import (
    CustomPasswordResetForm, UpdateProfilePicture, BioForm,
    ProfileForm, TrainerForm, AccountForm
    )


def signup_view(request):
    return render(request, 'signup.html')


def login_view(request):
    return render(request, 'login.html')


def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


@login_required
def update_profile(request):
    if request.method == 'POST':
        picture_form = UpdateProfilePicture(
            request.POST, request.FILES, instance=request.user, prefix='pic')
        bio_form = BioForm(
            request.POST, instance=request.user, prefix='bio')
        profile_form = ProfileForm(
            request.POST, instance=request.user, prefix='profile')
        trainer_form = TrainerForm(
            request.POST, instance=request.user, prefix='trainer')
        account_form = AccountForm(
            request.POST, instance=request.user, prefix='account')

        if 'update_picture' in request.POST and picture_form.is_valid():
            picture_form.save()
        elif 'update_profile' in request.POST and profile_form.is_valid():
            bio_form.save()
        elif 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
        elif 'update_trainer' in request.POST and trainer_form.is_valid():
            trainer_form.save()
        elif 'update_account' in request.POST and account_form.is_valid():
            account_form.save()
            return redirect('profile_updated')
    else:
        picture_form = UpdateProfilePicture(
            instance=request.user, prefix='pic')
        bio_form = BioForm(
            instance=request.user, prefix='bio')
        profile_form = ProfileForm(
            instance=request.user, prefix='profile')
        trainer_form = TrainerForm(
            instance=request.user, prefix='trainer')
        account_form = AccountForm(
            instance=request.user, prefix='account')

    context = {
        'picture_form': picture_form,
        'bio_form': bio_form,
        'profile_form': profile_form,
        'trainer_form': trainer_form,
        'account_form': account_form
    }
    return render(request, 'users/update_profile.html', context)
