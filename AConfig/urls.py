from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from MAuthentication import views

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^$", login_required(views.HomeView.as_view()), name="home-view"),
    path("", include('MAuthentication.urls')),
    path("", include('MChat.urls')),
    path('socialauth/', include('social_django.urls', namespace='social'))
]
