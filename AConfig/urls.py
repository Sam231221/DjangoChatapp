from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from MCore.views import home

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    path("", home, name="home-view"),
    path("", include('MCore.urls')),
    path("", include('MAuthentication.urls')),
    path("", include('MChat.urls')),
    path('socialauth/', include('social_django.urls', namespace='social'))
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)