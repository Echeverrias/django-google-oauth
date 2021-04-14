from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.urls import reverse
from profiles.models import User
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'GET':
        user_form = UserRegisterForm()
        return render(request, 'account/form.html', {'form': user_form})
    elif request.method == 'POST':
        user_form = UserRegisterForm(request.POST,  request.FILES, initial={'has_registered_with_this_app': True})
        if user_form.is_valid():
            user = user_form.save(commit=True) #user_form.save(commit=False)
            print(user)
            username, raw_password = user_form.cleaned_data.get('username'), user_form.cleaned_data.get('password1')
            #account = authenticate(username=username, password=raw_password)
            #login(request, account, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        return render(request, 'account/form.html', {'form': user_form})

def update_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        user_form = UserUpdateForm(instance=user, initial={'pk':pk})
        return render(request, 'account/form.html', {'form': user_form})
    elif request.method == 'POST':
        user_form = UserUpdateForm(request.POST,  request.FILES, instance=user)
        if user_form.is_valid():
            user = user_form.save()
            return redirect('get_user', pk=user.pk)
        return render(request, 'account/form.html', {'form': user_form})

def user_form_view(request):
    form = UserForm() #UserForm
    return render(request, 'account/form.html', {'form': form})

def login_view(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return auth_views.LoginView.as_view(authentication_form=UserLoginForm, template_name="account/form.html")(request)
