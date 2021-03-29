from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect

def my_logout(request):
    logout(request)
    return redirect('/city_swipe_app/')

urlpatterns = [
    url(r'^city_swipe_app/', include('city_swipe_app.urls')),
    url(r'^admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', my_logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
