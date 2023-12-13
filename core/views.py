from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/index.html')


def terms_view(request):
    return render(request, 'core/terms.html')
