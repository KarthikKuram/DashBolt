from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse,reverse_lazy
from django.views.generic import (TemplateView, CreateView)
from .forms import RegisterForm 
from .managers import Organization
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from dashboard.models import Tally_Detail,Ledger_Master, Custom_Category
# Create your views here.

class Login_page(LoginView):
    template_name = 'users/login.html'
   
class Register_page(CreateView):
    template_name = 'users/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_success')

    def form_valid(self,form):
        new_organization = form['organization'].save(commit=False)
        organization, created = Organization.objects.get_or_create(name = new_organization.name)
        new_user = form['user'].save(commit=False)
        new_user.organization = organization
        new_user.save()
        return redirect(self.success_url)
        
class Register_success(TemplateView):
    template_name = 'users/pending_access.html'

@login_required
def Dashboard_page(request):
    if not request.user.access:
        return render(request,'users/pending_access.html')
    
    elif timezone.now() > request.user.validity:
        return render(request, 'users/validity_expired.html')
    
    elif (not Tally_Detail.objects.filter(organization=request.user.organization).exists()) & request.user.org_admin:
        return redirect('tally_settings')
    
    elif (Custom_Category.objects.filter(organization=request.user.organization,primary_group__isnull = True).count()) > 0:
        return redirect('custom_group_list')
    
    else:
        return render(request,'dashboard/main.html')
    
class Logout_page(LogoutView):
    template_name = 'users/logout.html'