from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home_view(request):
    template_name = "index.html"
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, template_name)