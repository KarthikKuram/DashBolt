from django.views.generic import CreateView,UpdateView,RedirectView,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError, Sum
from .forms import Tally_Details_Form
from .models import Tally_Detail,Voucher_Ledgers
from django.urls import reverse_lazy, reverse
from django.shortcuts import render,redirect
from django.http import JsonResponse
import pandas as pd
from datetime import datetime,timedelta
import math

def find_digits(n):
    if n > 0:
        return int(math.log10(n)) + 1
    elif n == 0:
        return 1
    else:
        return int(math.log10(-n)) + 1

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
    
def update_dashboard(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_date_pd = datetime.strptime(start_date,'%Y-%m-%d')
    end_date_pd = datetime.strptime(end_date,'%Y-%m-%d')
    diff_days = (end_date_pd - start_date_pd).days
    previous_start_date = datetime.strftime((start_date_pd - timedelta(days=diff_days)),'%Y-%m-%d')
    previous_end_date = datetime.strftime((start_date_pd - timedelta(days=1)),'%Y-%m-%d')
    
    ### INCOME DASH CARD ###
    income_chart_labels = []
    income_chart_data = []
    try:
        present_income = round(Voucher_Ledgers.income.filter(voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)        
    except:
        present_income_denomination = ""
        present_income = 0
    try:        
        previous_income = round(Voucher_Ledgers.income.filter(voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)
    except:
        previous_income_denomination = ""
        previous_income = 0    
    try:
        perc_change_income = round((present_income - previous_income)/previous_income*100,2)
    except ZeroDivisionError:
        if present_income == 0:
            perc_change_income = 0
        else:
            perc_change_income = 100        
    try:
        income_entries = Voucher_Ledgers.income.filter(voucher_date__range=[start_date,end_date])\
            .values('voucher_date').annotate(total = Sum('amount')).order_by('voucher_date')
        for entry in income_entries:
            income_chart_labels.append(entry['voucher_date'])
            income_chart_data.append(float(entry['total']))          
    except:
        income_chart_labels = []
        income_chart_data = []
    
    digits = find_digits(present_income)
    if digits > 6:
        present_income = round(present_income/100000,2)
        present_income_denomination = " L"
    else:
        present_income_denomination = ""    
    
    digits = find_digits(previous_income)
    if digits > 6:
        previous_income_denomination = " L"
        previous_income = round(previous_income/100000,2)
    else:
        previous_income_denomination = ""         
        
    ### EXPENSE DASH CARD ###
    expense_chart_labels = []
    expense_chart_data = []
    try:
        present_expense = round(Voucher_Ledgers.expense.filter(voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        present_expense_denomination = ""
        present_expense = 0
    try:        
        previous_expense = round(Voucher_Ledgers.expense.filter(voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_expense_denomination = ""
        previous_expense = 0    
    try:
        perc_change_expense = round((present_expense - previous_expense)/previous_expense*100,2)
    except ZeroDivisionError:
        if present_expense == 0:
            perc_change_expense = 0
        else:
            perc_change_expense = 100        
    try:
        expense_entries = Voucher_Ledgers.expense.filter(voucher_date__range=[start_date,end_date])\
            .values('voucher_date').annotate(total = Sum('amount')).order_by('voucher_date')
        for entry in expense_entries:
            expense_chart_labels.append(entry['voucher_date'])
            expense_chart_data.append(float(entry['total'])*-1)          
    except:
        expense_chart_labels = []
        expense_chart_data = []
        
    digits = find_digits(present_expense)
    if digits > 6:
        present_expense = round(present_expense/100000,2)
        present_expense_denomination = " L"
    else:
        present_expense_denomination = ""                
    
    digits = find_digits(previous_expense)
    if digits > 6:
        previous_expense_denomination = " L"
        previous_expense = round(previous_expense/100000,2)
    else:
        previous_expense_denomination = ""    
   
    return JsonResponse(data={
      'present_income': present_income,
      'present_income_denomination' : present_income_denomination,
      'previous_income' : previous_income,
      'previous_income_denomination' : previous_income_denomination,
      'perc_change_income' : perc_change_income,
      'income_chart_labels' : income_chart_labels,
      'income_chart_data' : income_chart_data,
      'present_expense': present_expense,
      'present_expense_denomination' : present_expense_denomination,
      'previous_expense' : previous_expense,
      'previous_expense_denomination' : previous_expense_denomination,
      'perc_change_expense' : perc_change_expense,
      'expense_chart_labels' : expense_chart_labels,
      'expense_chart_data' : expense_chart_data,
    })