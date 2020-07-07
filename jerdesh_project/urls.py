from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import urls
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
	path('', include('jerdesh.urls')),
	path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    prefix_default_language=False,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
