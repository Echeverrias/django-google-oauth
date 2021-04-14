
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('logout/', RedirectView.as_view(pattern_name='logout', permanent=True)),
    path('signup/', RedirectView.as_view(url='/account/register/', permanent=True)),
    path('', include('allauth.urls')),
]

