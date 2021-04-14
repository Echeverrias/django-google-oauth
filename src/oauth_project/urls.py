from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from . import settings
from .views import home_view
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
    path('account/', include('account.urls')),
    path('oauth/', include('oauth_app.urls')),
    path('home/', home_view, name='home'),
    path('login/', RedirectView.as_view(url='/account/login', permanent=True), name='login'),
    path('register/', RedirectView.as_view(url='/account/register', permanent=True), name='register'),
    re_path(r'^$', RedirectView.as_view(url='/home', permanent=True), name='home'),
    path('', RedirectView.as_view(url='/home', permanent=True), name='home'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
