from django.shortcuts import render


def index(request):
    """
    Render the index.html template
    """
    return render(request, 'core/index.html')
