
from django.urls import path, include, re_path
from .views import register_view, update_view, login_view
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [

    path('register/', register_view, name='register'),
    path('update/<int:pk>/', update_view, name='update'),
    path('login/',  login_view , name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

