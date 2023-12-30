from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import CustomPasswordResetForm
from django.contrib.auth import logout
from .forms import UserProfileForm


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


@login_required
def account_view(request):
    """
    View for viewing user profile
    """
    if request.user.is_authenticated:
        form = UserProfileForm(instance=request.user)
        return render(request, 'account/account.html', {'form': form})
    else:
        # Handle unauthenticated user, maybe redirect to login page
        pass


@login_required
def update_profile(request):
    """
    View for updating user profile, redirects to the
    account view upon successful update.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST,
                               request.FILES,
                               instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'account/settings.html', {'form': form})
