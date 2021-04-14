from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User

# Create your views here.
def get_user_view(request, pk):
    if (not request.user.is_authenticated or request.user.pk != pk):
        return HttpResponseRedirect(reverse('home') )
    user = User.objects.get(pk=pk)
    return render(request, 'profiles/user.html', {'user': user})