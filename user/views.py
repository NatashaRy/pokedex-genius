from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from .forms import SignUpForm


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('pokedex/dashboard.html')
#         else:
#             # Invalid login
#             pass
#     return render(request, 'account/login.html')


# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect after successful sign up
#             return redirect('accounts/signup.html')
#     else:
#         form = SignUpForm()
#     return render(
#         request, 'accounts/signup.html', {'form': form})
