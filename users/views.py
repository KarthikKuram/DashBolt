from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, CreateView)
from .forms import NewUserForm 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
# Create your views here.

class Login_page(LoginView):
    template_name = 'users/login.html'
   
class Register_page(CreateView):
    template_name = 'users/sign_up.html'
    form_class = NewUserForm
    success_url = reverse_lazy('register_success')

class Register_success(TemplateView):
    template_name = 'users/pending_access.html'

@login_required
def Dashboard_page(request):
    if not request.user.access:
        return render(request,'users/pending_access.html')
    
    elif timezone.now() > request.user.validity:
        return render(request, 'users/validity_expired.html')
    else:
        return render(request,'dashboard/main.html')
    
class Logout_page(LogoutView):
    template_name = 'users/logout.html'
    