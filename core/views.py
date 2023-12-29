from django.shortcuts import render, redirect


def index(request):
    """
    Index page
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/index.html')


def terms_view(request):
    """
    Terms of use page
    """
    return render(request, 'core/terms.html')


def custom_404(request, exception):
    """
    Custom 404 page
    """
    return render(request, 'core/404.html', {}, status=404)
