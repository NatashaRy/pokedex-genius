from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='core-urls'),
    path('', include('pokedex.urls')),
    path('', include('users.urls')),
    path('accounts/', include('allauth.urls')),
]

handler404 = 'core.views.custom_404'

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
