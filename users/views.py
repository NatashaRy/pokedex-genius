from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordChangeView,
    )
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import (
    CustomPasswordResetForm,
    CustomLoginForm, 
    CustomSignupForm,
    )
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import logout as auth_logout
from .forms import UserProfileForm


# ============================================================
# LOGIN/SIGNUP/LOGOUT
# ============================================================

def login_view(request):
    print("### Min login_view körs!")
    """
    View for user login
    """
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Set session expiry based on remember me
                if not remember:
                    request.session.set_expiry(0)
                
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    
    context = {
        'form': form,
        'signup_url': '/signup/'
    }
    return render(request, 'account/login.html', context)


def signup_view(request):
    """
    View for user signup
    """
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}!')
            
            # Automatically log in the user after signup
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomSignupForm()
    
    context = {
        'form': form,
        'login_url': '/login/'
    }
    return render(request, 'account/signup.html', context)


def logout_view(request):
    """
    View for user logout
    """
    auth_logout(request)
    return redirect('index')


# ============================================================
# PASSWORD
# ============================================================

class CustomPasswordResetView(PasswordResetView):
    template_name = "account/password_reset.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('password_change')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)


# ============================================================
# ACCOUNT
# ============================================================

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
