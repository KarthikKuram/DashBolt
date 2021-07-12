from django.views.generic import CreateView,UpdateView,RedirectView,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from .forms import Tally_Details_Form
from .models import Tally_Detail
from django.urls import reverse_lazy, reverse
from django.shortcuts import render,redirect

class Tally_Details_Redirect(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self):
        if Tally_Detail.objects.filter(organization=self.request.user.organization).exists():
            return reverse('dashboard')
        else:
            return reverse('tally_settings')

class Tally_Details_List(LoginRequiredMixin,ListView):
    model = Tally_Detail
    
    def get_queryset(self):
        qs = super(Tally_Details_List,self).get_queryset()
        return qs.filter(organization = self.request.user.organization)
    
class Tally_Details_CreateView(LoginRequiredMixin,CreateView):
    model = Tally_Detail
    form_class = Tally_Details_Form
    template_name = 'dashboard/tally_settings.html'
    success_url = reverse_lazy('tally_settings')
    
    def get_form(self):
        obj = Tally_Detail.objects.filter(organization=self.request.user.organization).first()
        if not obj:
            form = super(Tally_Details_CreateView,self).get_form()
            return form
        else:
            form = super(Tally_Details_CreateView,self).get_form()
            form.fields['account_id'].disabled = True
            form.fields['computer_name'].disabled = True
            return form
            
    def get_initial(self):
        obj = Tally_Detail.objects.filter(organization=self.request.user.organization).first()
        if not obj:
            initial = super(Tally_Details_CreateView,self).get_initial()
            return initial
        else:
            initial = super(Tally_Details_CreateView,self).get_initial()
            initial['account_id'] = obj.account_id
            initial['computer_name'] = obj.computer_name
            return initial
    
    def form_valid(self, form):
        first_entry = Tally_Detail.objects.filter(organization=self.request.user.organization).first()
        if not first_entry:
            obj = form.save(commit=False)
            obj.organization = self.request.user.organization
            obj.save()
            messages.success(self.request,"New tally settings created.")
            return super(Tally_Details_CreateView, self).form_valid(form)
        else:
            obj = form.save(commit=False)
            obj.organization = self.request.user.organization
            obj.account_id = first_entry.account_id
            obj.computer_name = first_entry.computer_name
            obj.save()
            messages.success(self.request,"New tally settings created with modifications.")
            return super(Tally_Details_CreateView, self).form_valid(form)
    
class Tally_Details_UpdateView(LoginRequiredMixin,UpdateView):
    model = Tally_Detail
    fields = ['name','tally_begin_date','tally_port']
    template_name = 'dashboard/tally_edit_settings.html'
    success_url = reverse_lazy('tally_settings')
    
    def form_valid(self, form):
        messages.success(self.request,"Tally settings updated.")
        return super(Tally_Details_UpdateView, self).form_valid(form)
    
class Tally_Details_DeleteView(LoginRequiredMixin,DeleteView):
    model = Tally_Detail
    success_url = reverse_lazy('tally_settings')
    error_template = 'dashboard/tally_detail_list.html'
    
    def post(self, request, *args, **kwargs):
        try:
            post = self.delete(request, *args, **kwargs)
            messages.success(request,"Tally settings deleted.",extra_tags='success')
            return post
        except ProtectedError:
            messages.error(request,"You cannot delete this setting",extra_tags='danger')
            return redirect('tally_settings')

        return render(request,self.success_url,{})