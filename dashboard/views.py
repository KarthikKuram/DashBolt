from django.views.generic import CreateView,UpdateView,RedirectView,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError, Sum, Q, Count,Min,Case,Value,When,FloatField,DateField,ExpressionWrapper,F,IntegerField,CharField
from django.db.models.functions import Cast,ExtractDay,TruncDate,TruncMonth
from .forms import Tally_Details_Form, Tally_Valid_Users_Form
from .models import Tally_Detail,Voucher_Ledgers,Ledger_Master,Voucher_Bills,Voucher_CostCenters
from django.urls import reverse_lazy, reverse
from django.shortcuts import render,redirect
from django.http import JsonResponse
import pandas as pd
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import math

def find_digits(n):
    if n > 0:
        return int(math.log10(n)) + 1
    elif n == 0:
        return 1
    else:
        return int(math.log10(-n)) + 1

class Tally_Details_List(LoginRequiredMixin,ListView):
    model = Tally_Detail
    
    def get_queryset(self):
        qs = super(Tally_Details_List,self).get_queryset()
        return qs.filter(organization = self.request.user.organization)
    
class Tally_Valid_Users(LoginRequiredMixin,UpdateView):
    model = Tally_Detail
    form_class = Tally_Valid_Users_Form
    template_name = 'dashboard/tally_valid_users.html'
    success_url = reverse_lazy('tally_settings')
    
    def get_form_kwargs(self):
        kwargs = super(Tally_Valid_Users,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        messages.success(self.request,"User Access updated.")
        return super(Tally_Valid_Users, self).form_valid(form)        
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
    diff_days = (end_date_pd - start_date_pd).days + 1
    previous_start_date = datetime.strftime((start_date_pd - timedelta(days=diff_days)),'%Y-%m-%d')
    previous_end_date = datetime.strftime((start_date_pd - timedelta(days=1)),'%Y-%m-%d')
    
    ### INCOME AND TOP 5 INCOME ACCOUNTS DASH CARD ###
    income_chart_labels = []
    income_chart_data = []
    income_ledgers_chart_labels = []
    income_ledgers_chart_data = []
    present_top_income_ledgers = {}
    previous_top_income_ledgers = {}
    perc_change_top_income_ledgers = {}
    try:
        income_dump = Voucher_Ledgers.income.filter(voucher_date__range=[start_date,end_date])
        present_income = round(income_dump.aggregate(Sum('amount'))['amount__sum'],0)
        income_voucher_list = income_dump.values_list('voucher_key', flat=True) 
        present_income_ledgers = income_dump.values('ledger').annotate(total=Sum('amount')).order_by('-total')[:5]
        for entry in present_income_ledgers:
            income_ledgers_chart_labels.append(entry['ledger'])
            income_ledgers_chart_data.append(round(float(entry['total']),0))
            present_top_income_ledgers[entry['ledger']] = round(float(entry['total']),0)
    except:
        present_income = 0
        income_voucher_list = []      
    
    present_gross_profit = present_income
    
    try:
        previous_income_dump =  Voucher_Ledgers.income.filter(voucher_date__range=[previous_start_date,previous_end_date])
        previous_income = round(previous_income_dump.aggregate(Sum('amount'))['amount__sum'],0)        
        previous_income_ledgers = Voucher_Ledgers.objects.filter(ledger__in = income_ledgers_chart_labels,
                                                                 voucher_date__range=[previous_start_date,previous_end_date]).\
                                                                     values('ledger').annotate(total=Sum('amount'))
        for entry in previous_income_ledgers:
            previous_top_income_ledgers[entry['ledger']] = round(float(entry['total']),0)
    except:
        previous_income = 0    
    
    for entry in income_ledgers_chart_labels:  
        try:
            perc_change_top_income_ledgers[entry] = round((present_top_income_ledgers[entry] - previous_top_income_ledgers[entry])/abs(previous_top_income_ledgers[entry])*100,0)
        except:
            if present_top_income_ledgers[entry] == 0:
                perc_change_top_income_ledgers[entry]= 0
            else:
                perc_change_top_income_ledgers[entry]= 100        
    
    previous_gross_profit = previous_income
    
    try:
        perc_change_income = round((present_income - previous_income)/abs(previous_income)*100,2)
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
            income_chart_data.append(round(float(entry['total']),0))
    except:
        income_chart_labels = []
        income_chart_data = []
    
    ### EXPENSE AND TOP 5 EXPENSE ACCOUNTS DASH CARD ###
    expense_chart_labels = []
    expense_chart_data = []
    expense_ledgers_chart_labels=[]
    expense_ledgers_chart_data=[]
    present_top_expense_ledgers = {}
    previous_top_expense_ledgers = {}
    perc_change_top_expense_ledgers = {}
    try:
        expense_dump = Voucher_Ledgers.expense.filter(voucher_date__range=[start_date,end_date])
        present_expense = round(expense_dump.aggregate(Sum('amount'))['amount__sum'],0)*-1
        expense_voucher_list = expense_dump.values_list('voucher_key', flat=True)
        present_expense_ledgers = expense_dump.values('ledger').annotate(total=Sum('amount')).order_by('total')[:5]
        for entry in present_expense_ledgers:
            expense_ledgers_chart_labels.append(entry['ledger'])
            expense_ledgers_chart_data.append(round(float(entry['total']),0)*-1)
            present_top_expense_ledgers[entry['ledger']] = round(float(entry['total']),0)*-1
    except:
        present_expense = 0
        expense_voucher_list = []
    try:        
        previous_expense_dump = Voucher_Ledgers.expense.filter(voucher_date__range=[previous_start_date,previous_end_date])
        previous_expense = round(previous_expense_dump.aggregate(Sum('amount'))['amount__sum'],0)*-1
        previous_expense_ledgers = Voucher_Ledgers.objects.filter(ledger__in = expense_ledgers_chart_labels,
                                                                 voucher_date__range=[previous_start_date,previous_end_date]).\
                                                                     values('ledger').annotate(total=Sum('amount'))
        for entry in previous_expense_ledgers:
            previous_top_expense_ledgers[entry['ledger']] = round(float(entry['total']),0)*-1                                                                   
    except:
        previous_expense = 0    
        
    for entry in expense_ledgers_chart_labels:
        try:
            perc_change_top_expense_ledgers[entry] = round((present_top_expense_ledgers[entry] - previous_top_expense_ledgers[entry])/abs(previous_top_expense_ledgers[entry])*100,0)
        except:
            if present_top_expense_ledgers[entry] == 0:
                perc_change_top_expense_ledgers[entry]=0
            else:
                perc_change_top_expense_ledgers[entry] = 100    
            
    try:
        perc_change_expense = round((present_expense - previous_expense)/abs(previous_expense)*100,2)
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
            expense_chart_data.append(round(float(entry['total'])*-1,0))
    except:
        expense_chart_labels = []
        expense_chart_data = []
        
    ### RECEIVABLE & PAYABLE DASH CARD ###
    recpay_chart_data = []
    try:
        present_debtor = round(Voucher_Ledgers.debtor.filter(voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
        recpay_chart_data.append(float(present_debtor))          
        
    except:
        present_debtor = 0
        recpay_chart_data.append(float(present_debtor))
    
    try:
        present_creditor = round(Voucher_Ledgers.creditor.filter(voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)
        recpay_chart_data.append(float(present_creditor))
    except:
        present_creditor = 0
        recpay_chart_data.append(float(present_creditor))
    try:        
        previous_debtor = round(Voucher_Ledgers.debtor.filter(voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_debtor = 0    
    try:        
        previous_creditor = round(Voucher_Ledgers.creditor.filter(voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)
    except:
        previous_creditor = 0    
    try:
        perc_change_debtor = round((present_debtor - previous_debtor)/abs(previous_debtor)*100,2)
    except ZeroDivisionError:
        if present_debtor == 0:
            perc_change_debtor = 0
        else:
            perc_change_debtor = 100        
    try:
        perc_change_creditor = round((present_creditor - previous_creditor)/abs(previous_creditor)*100,2)
    except ZeroDivisionError:
        if present_creditor == 0:
            perc_change_creditor = 0
        else:
            perc_change_creditor = 100        
    
    
    ### AGEING SCHEDULE WORKINGS ###
    ageing_labels = ['0-30','31-90','91-120','>>120','On Account']
    receivable_ageing_value = []
    receivable_ageing_count = []
    payable_ageing_value = []
    payable_ageing_count = []
    
    # receivable ageing
    debtor_bills_ref = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors").exclude(bill_type = "On Account").\
        values('bill_name').annotate(
            bill_date = Min('voucher_date'),
            net_due = Sum('bill_amount')*-1,
            cutoff_date = Value(end_date_pd,output_field=DateField()),
            age=Cast(ExtractDay(TruncDate(F('cutoff_date')) - TruncDate(F('bill_date'))),output_field = IntegerField()),
            age_group = Case(
                        When(age__range = [0,30],then = Value('0-30')),
                        When(age__range = [31,90],then = Value('31-90')),
                        When(age__range = [91,120],then = Value('91-120')),
                        When(age__gt = 120,then = Value('>>120')),
                        default = Value('No Group'),
                        output_field = CharField()
                    )
            ).filter(net_due__gt = 0).values_list('age_group','net_due')
    debtor_bills_ref = pd.DataFrame(debtor_bills_ref,columns = ['Age_Group','Due'])
    debtor_bills_ref = debtor_bills_ref.groupby('Age_Group').Due.agg(['sum','count']).reset_index()
    
    # payable ageing
    creditor_bills_ref = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Creditors").exclude(bill_type = "On Account").\
        values('bill_name').annotate(
            bill_date = Min('voucher_date'),
            net_due = Sum('bill_amount'),
            cutoff_date = Value(end_date_pd,output_field=DateField()),
            age=Cast(ExtractDay(TruncDate(F('cutoff_date')) - TruncDate(F('bill_date'))),output_field = IntegerField()),
            age_group = Case(
                        When(age__range = [0,30],then = Value('0-30')),
                        When(age__range = [31,90],then = Value('31-90')),
                        When(age__range = [91,120],then = Value('91-120')),
                        When(age__gt = 120,then = Value('>>120')),
                        default = Value('No Group'),
                        output_field = CharField()
                    )
            ).filter(net_due__gt = 0).values_list('bill_name','age_group','net_due')
    creditor_bills_ref = pd.DataFrame(creditor_bills_ref,columns = ['Bill Name','Age_Group','Due'])
    creditor_bills_ref = creditor_bills_ref.groupby('Age_Group').Due.agg(['sum','count']).reset_index()
    
    # On Account Entries
    debtor_bills_onaccount = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors",bill_type = "On Account").\
        values('bill_name').annotate(bill_type = Value('On Account'), net_due = Sum('bill_amount')*-1, count = Count('bill_amount')).\
            filter(net_due__gt = 0).values_list('bill_type','net_due','count')        
            
    debtor_bills_onaccount_reverse = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors",bill_type = "On Account").\
        values('bill_name').annotate(bill_type = Value('On Account'), net_due = Sum('bill_amount'), count = Count('bill_amount')).\
            filter(net_due__gt = 0).values_list('bill_type','net_due','count')                
            
    
    creditor_bills_onaccount = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Creditors",bill_type = "On Account").\
        values('bill_name').annotate(bill_type = Value('On Account'), net_due = Sum('bill_amount'), count = Count('bill_amount')).\
            filter(net_due__gt = 0).values_list('bill_type','net_due','count')        
    
    creditor_bills_onaccount_reverse = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Creditors",bill_type = "On Account").\
        values('bill_name').annotate(bill_type = Value('On Account'), net_due = Sum('bill_amount')*-1, count = Count('bill_amount')).\
            filter(net_due__gt = 0).values_list('bill_type','net_due','count')        

    
    if debtor_bills_onaccount.exists():
        debtor_bills_onaccount = pd.DataFrame(debtor_bills_onaccount,columns = ['Age_Group','sum','count'])
    else:
        debtor_bills_onaccount = pd.DataFrame(columns = ['Age_Group','sum','count'])
    
    if creditor_bills_onaccount.exists():
        creditor_bills_onaccount = pd.DataFrame(creditor_bills_onaccount,columns = ['Age_Group','sum','count'])
    else:
        creditor_bills_onaccount = pd.DataFrame(columns = ['Age_Group','sum','count'])
    
    if debtor_bills_onaccount_reverse.exists():
        debtor_bills_onaccount_reverse = pd.DataFrame(debtor_bills_onaccount_reverse,columns = ['Age_Group','sum','count'])
    else:
        debtor_bills_onaccount_reverse = pd.DataFrame(columns = ['Age_Group','sum','count'])
    
    if creditor_bills_onaccount_reverse.exists():
        creditor_bills_onaccount_reverse = pd.DataFrame(creditor_bills_onaccount_reverse,columns = ['Age_Group','sum','count'])
    else:
        creditor_bills_onaccount_reverse = pd.DataFrame(columns = ['Age_Group','sum','count'])
    
    # create consolidated dataframe for On Account Entries #
    debtor_bills_onaccount = debtor_bills_onaccount.append(creditor_bills_onaccount_reverse,ignore_index=True)
    creditor_bills_onaccount = creditor_bills_onaccount.append(debtor_bills_onaccount_reverse,ignore_index = True)
    
    debtor_bills_onaccount = debtor_bills_onaccount.groupby('Age_Group').agg({'sum':'sum', 'count':'sum'}).reset_index()
    creditor_bills_onaccount = creditor_bills_onaccount.groupby('Age_Group').agg({'sum':'sum', 'count':'sum'}).reset_index()  
    
    # Append to ageing summary
    debtor_bills_ref = debtor_bills_ref.append(debtor_bills_onaccount,ignore_index = True)
    creditor_bills_ref = creditor_bills_ref.append(creditor_bills_onaccount,ignore_index = True)
    
    
    for entry in ageing_labels:
        try:
            receivable_ageing_value.append(round(float(debtor_bills_ref[debtor_bills_ref['Age_Group']==entry]['sum'].iloc[0]),0))
            receivable_ageing_count.append(int(debtor_bills_ref[debtor_bills_ref['Age_Group']==entry]['count'].iloc[0]))
        except:
            receivable_ageing_value.append(0)    
            receivable_ageing_count.append(0)
    
    for entry in ageing_labels:
        try:
            payable_ageing_value.append(round(float(creditor_bills_ref[creditor_bills_ref['Age_Group']==entry]['sum'].iloc[0]),0))
            payable_ageing_count.append(int(creditor_bills_ref[creditor_bills_ref['Age_Group']==entry]['count'].iloc[0]))
        except:
            payable_ageing_value.append(0)    
            payable_ageing_count.append(0)    
        
    ### CASH & BANK DASH CARD ###
    cashbank_chart_data = []
    try:
        present_cash_dump = Voucher_Ledgers.cash.filter(voucher_date__range=[start_date,end_date])
        present_cash = round(present_cash_dump.aggregate(Sum('amount'))['amount__sum'],0)*-1        
        cashbank_chart_data.append(float(present_cash))
    except:
        present_cash = 0
        cashbank_chart_data.append(float(present_cash))
    try:
        previous_cash_dump = Voucher_Ledgers.cash.filter(voucher_date__range=[previous_start_date,previous_end_date])
        previous_cash = round(previous_cash_dump.aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_cash = 0
    try:
        present_bank_dump = Voucher_Ledgers.bank.filter(voucher_date__range=[start_date,end_date])
        present_bank = round(present_bank_dump.aggregate(Sum('amount'))['amount__sum'],0)*-1
        cashbank_chart_data.append(float(present_bank))
    except:
        present_bank = 0
        cashbank_chart_data.append(float(present_bank))
    try:
        previous_bank_dump = Voucher_Ledgers.bank.filter(voucher_date__range=[previous_start_date,previous_end_date])
        previous_bank = round(previous_bank_dump.aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_bank = 0
    try:
        perc_change_cash = round((present_cash - previous_cash)/abs(previous_cash)*100,2)
    except ZeroDivisionError:
        if present_cash == 0:
            perc_change_cash = 0
        else:
            perc_change_cash = 100        
    try:
        perc_change_bank = round((present_bank - previous_bank)/abs(previous_bank)*100,2)
    except ZeroDivisionError:
        if present_bank == 0:
            perc_change_bank = 0
        else:
            perc_change_bank = 100        
    
    # Cash Receipts Entries
    receipts_payments_labels_date = []
    receipts_payments_labels = []
    cash_receipts_value = []
    cash_payments_value = []
    bank_receipts_value = []
    bank_payments_value = []
    
    # begin_date = (datetime.strptime(end_date,'%Y-%m-%d') + relativedelta(months = -5)).replace(day=1).strftime('%Y-%m-%d')
    begin_date = (datetime.strptime(end_date,'%Y-%m-%d') + relativedelta(months = -5)).replace(day=1)
    # Get Last 6 Months Label
    for i in range (6):
        receipts_payments_labels_date.append((begin_date + relativedelta(months = i)).date())
           
    cash_receipts_dump = Voucher_Ledgers.cash.filter(voucher_date__range=[begin_date,end_date],amount__lt = 0)
    cash_receipts = cash_receipts_dump.annotate(month = TruncMonth('voucher_date')).\
        values('month').annotate(amount = Sum('amount')*-1)
    cash_receipts = pd.DataFrame(cash_receipts,columns = ['month','amount'])
    
    cash_payments_dump = Voucher_Ledgers.cash.filter(voucher_date__range=[begin_date,end_date],amount__gt = 0)
    cash_payments = cash_payments_dump.annotate(month = TruncMonth('voucher_date')).\
        values('month').annotate(amount = Sum('amount'))
    cash_payments = pd.DataFrame(cash_payments,columns = ['month','amount'])
       
    bank_receipts_dump = Voucher_Ledgers.bank.filter(voucher_date__range=[begin_date,end_date],amount__lt = 0)
    bank_receipts = bank_receipts_dump.annotate(month = TruncMonth('voucher_date')).\
        values('month').annotate(amount = Sum('amount')*-1)
    bank_receipts = pd.DataFrame(bank_receipts,columns = ['month','amount'])
    
    bank_payments_dump = Voucher_Ledgers.bank.filter(voucher_date__range=[begin_date,end_date],amount__gt = 0)
    bank_payments = bank_payments_dump.annotate(month = TruncMonth('voucher_date')).\
        values('month').annotate(amount = Sum('amount'))
    bank_payments = pd.DataFrame(bank_payments,columns = ['month','amount'])
    
    for entry in receipts_payments_labels_date:
        try:
            cash_receipts_value.append(round(float(cash_receipts[cash_receipts['month']==entry]['amount'].iloc[0]),0))
            receipts_payments_labels.append(entry.strftime('%b-%Y'))
        except:
            receipts_payments_labels.append(entry.strftime('%b-%Y'))
            cash_receipts_value.append(0)        
        try:
            cash_payments_value.append(round(float(cash_payments[cash_payments['month']==entry]['amount'].iloc[0]),0))
        except:
            cash_payments_value.append(0)        
        try:
            bank_receipts_value.append(round(float(bank_receipts[bank_receipts['month']==entry]['amount'].iloc[0]),0))
        except:
            bank_receipts_value.append(0)        
        try:
            bank_payments_value.append(round(float(bank_payments[bank_payments['month']==entry]['amount'].iloc[0]),0))
        except:
            bank_payments_value.append(0)            
        
    ### P&L MOVEMENT DASH CARD ###
    pl_chart_data = []
    try:
        present_direct_expense = round(Voucher_Ledgers.expense.filter(
            Q(ledger_primary_group='Purchase Accounts') | Q(ledger_primary_group='Direct Expenses') | Q(ledger_primary_group='Expenses (Direct)'),
            voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        present_direct_expense = 0    
    
    present_gross_profit-=present_direct_expense    
    
    try:
        previous_direct_expense = round(Voucher_Ledgers.expense.filter(
            Q(ledger_primary_group='Purchase Accounts') | Q(ledger_primary_group='Direct Expenses') | Q(ledger_primary_group='Expenses (Direct)'),
            voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_direct_expense = 0    
        
    previous_gross_profit-=previous_direct_expense    
        
    try:
        perc_change_direct_expense = round((present_direct_expense - previous_direct_expense)/abs(previous_direct_expense)*100,2)
    except ZeroDivisionError:
        if present_direct_expense == 0:
            perc_change_direct_expense = 0
        else:
            perc_change_direct_expense = 100

    try:
        perc_change_gross_profit = round((present_gross_profit - previous_gross_profit)/abs(previous_gross_profit)*100,2)
    except ZeroDivisionError:
        if present_gross_profit == 0:
            perc_change_gross_profit = 0
        else:
            perc_change_gross_profit = 100
            
    try:
        present_indirect_expense = round(Voucher_Ledgers.expense.filter(
            Q(ledger_primary_group='Indirect Expenses') | Q(ledger_primary_group='Expenses (Indirect)'),
            voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        present_indirect_expense = 0    
    try:
        previous_indirect_expense = round(Voucher_Ledgers.expense.filter(
            Q(ledger_primary_group='Indirect Expenses') | Q(ledger_primary_group='Expenses (Indirect)'),
            voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_indirect_expense = 0    
    try:
        perc_change_indirect_expense = round((present_indirect_expense - previous_indirect_expense)/abs(previous_indirect_expense)*100,2)
    except ZeroDivisionError:
        if present_indirect_expense == 0:
            perc_change_indirect_expense = 0
        else:
            perc_change_indirect_expense = 100
    
    present_net_profit = present_gross_profit - present_indirect_expense
    previous_net_profit = previous_gross_profit - previous_indirect_expense
    try:
        perc_change_net_profit = round((present_net_profit - previous_net_profit)/abs(previous_net_profit)*100,2)
    except ZeroDivisionError:
        if present_net_profit == 0:
            perc_change_net_profit = 0
        else:
            perc_change_net_profit = 100
    
    pl_chart_data.extend([present_income,present_direct_expense,present_gross_profit,present_indirect_expense,present_net_profit])
    
    ### TOP 5 CUSTOMERS DASH CARD ###
    top_customer_chart_labels = []
    top_customer_chart_total = []
    top_customer_chart_count = []
    try:
        top_customers = Voucher_Ledgers.objects.filter(voucher_key__in = income_voucher_list, ledger_primary_group='Sundry Debtors').values('ledger')\
            .annotate(total=Sum('amount'),inv_count=Count('ledger')).order_by('total')[:5]
        for entry in top_customers:
            top_customer_chart_labels.append(entry['ledger'])
            top_customer_chart_total.append(round(float(entry['total'])*-1,0))
            top_customer_chart_count.append(float(entry['inv_count']))
        
        # Get Opening Balance for Receivable Calculations #    
        opening_balances = Ledger_Master.objects.filter(ledger__in= top_customer_chart_labels).values('ledger','opening_balance')
        present_party_receivables = {}
        previous_party_receivables = {}
        perc_change_party_receivables = {}
        for entry in opening_balances:
            present_party_receivables[entry['ledger']] = round(float(entry['opening_balance'])*-1,0)
            previous_party_receivables[entry['ledger']] = round(float(entry['opening_balance'])*-1,0)
        
        # Get Net Transactions from the beginning till the last day of present period #
        net_transactions_present = Voucher_Ledgers.objects.filter(
            ledger__in= top_customer_chart_labels,
            voucher_date__lte=end_date).values('ledger').annotate(net=Sum('amount'))
        for entry in net_transactions_present:
            present_party_receivables[entry['ledger']]+=round(float(entry['net'])*-1,0)
        
        # Get Net Transactions from the beginning till the last day of previous period #
        net_transactions_previous = Voucher_Ledgers.objects.filter(
            ledger__in= top_customer_chart_labels,
            voucher_date__lte=previous_end_date).values('ledger').annotate(net=Sum('amount'))
        for entry in net_transactions_previous:
            previous_party_receivables[entry['ledger']]+=round(float(entry['net'])*-1,0)
        
        for entry in top_customer_chart_labels:  
            try:
                perc_change_party_receivables[entry] = round((present_party_receivables[entry] - previous_party_receivables[entry])/abs(previous_party_receivables[entry])*100,0)
            except ZeroDivisionError:
                if present_party_receivables[entry] == 0:
                    perc_change_party_receivables[entry]= 0
                else:
                    perc_change_party_receivables[entry]= 100
    except:
        pass
    
    ### TOP 5 VENDORS DASH CARD ###
    top_vendor_chart_labels = []
    top_vendor_chart_total = []
    top_vendor_chart_count = []
    try:
        top_vendors = Voucher_Ledgers.objects.filter(voucher_key__in = expense_voucher_list, ledger_primary_group='Sundry Creditors').values('ledger')\
            .annotate(total=Sum('amount'),inv_count=Count('ledger')).order_by('-total')[:5]
        for entry in top_vendors:
            top_vendor_chart_labels.append(entry['ledger'])
            top_vendor_chart_total.append(round(float(entry['total']),0))
            top_vendor_chart_count.append(float(entry['inv_count']))
        
        # Get Opening Balance for Payable Calculations #    
        opening_balances = Ledger_Master.objects.filter(ledger__in= top_vendor_chart_labels).values('ledger','opening_balance')
        present_party_payables = {}
        previous_party_payables = {}
        perc_change_party_payables = {}
        for entry in opening_balances:
            present_party_payables[entry['ledger']] = round(float(entry['opening_balance']),0)
            previous_party_payables[entry['ledger']] = round(float(entry['opening_balance']),0)
        
        # Get Net Transactions from the beginning till the last day of present period #
        net_transactions_present = Voucher_Ledgers.objects.filter(
            ledger__in= top_vendor_chart_labels,
            voucher_date__lte=end_date).values('ledger').annotate(net=Sum('amount'))
        for entry in net_transactions_present:
            present_party_payables[entry['ledger']]+=round(float(entry['net']),0)
        
        # Get Net Transactions from the beginning till the last day of previous period #
        net_transactions_previous = Voucher_Ledgers.objects.filter(
            ledger__in= top_vendor_chart_labels,
            voucher_date__lte=previous_end_date).values('ledger').annotate(net=Sum('amount'))
        for entry in net_transactions_previous:
            previous_party_payables[entry['ledger']]+=round(float(entry['net']),0)
        
        for entry in top_vendor_chart_labels:  
            try:
                perc_change_party_payables[entry] = round((present_party_payables[entry] - previous_party_payables[entry])/abs(previous_party_payables[entry])*100,0)
            except ZeroDivisionError:
                if present_party_payables[entry] == 0:
                    perc_change_party_payables[entry]= 0
                else:
                    perc_change_party_payables[entry]= 100
    except:
        pass
    
    ### TOP 5 COST CENTERS DASH CARD ###
    cc_category_chart_labels=[]
    cc_category_chart_data=[]
    present_top_cc_category = {}
    previous_top_cc_category = {}
    perc_change_top_cc_category = {}
    
    try:
        present_cc_dump = Voucher_CostCenters.objects.filter(
        (Q(ledger_category = 'Income') | Q(ledger_category = 'Expense')),
            voucher_date__range=[start_date,end_date])
        present_cc_category = present_cc_dump.values('cc_category').annotate(total=Sum('cc_amount')).\
            filter(total__gt = 0).order_by('-total')[:5]
        
        for entry in present_cc_category:
            cc_category_chart_labels.append(entry['cc_category'])
            cc_category_chart_data.append(round(float(entry['total']),0))
            present_top_cc_category[entry['cc_category']] = round(float(entry['total']),0)
    except:
        pass
    
    try:
        previous_cc_category = Voucher_CostCenters.objects.filter(
            (Q(ledger_category = 'Income') | Q(ledger_category = 'Expense')),
            cc_category__in = cc_category_chart_labels,
            voucher_date__range=[previous_start_date,previous_end_date]).\
            values('cc_category').annotate(total=Sum('cc_amount'))
        
        for entry in previous_cc_category:
            previous_top_cc_category[entry['cc_category']] = round(float(entry['total']),0)
    except:
        pass
        
    for entry in cc_category_chart_labels:
        try:
            perc_change_top_cc_category[entry] = round((present_top_cc_category[entry] - previous_top_cc_category[entry])/abs(previous_top_cc_category[entry])*100,0)
        except:
            if present_top_cc_category[entry] == 0:
                perc_change_top_cc_category[entry]=0
            else:   
                perc_change_top_cc_category[entry] = 100    
    
    ### CALCULATION OF FINANCIAL RATIOS ###
    # Current Ratio #
    current_assets = round(max((Voucher_Ledgers.objects.filter(Q(ledger_primary_group = "Current Assets")\
        | Q(ledger_grand_parent = "Current Assets")\
            | Q(ledger_parent = "Current Assets"),voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'])*-1,0),0)
    current_liabilities = round(max(Voucher_Ledgers.objects.filter(Q(ledger_primary_group = "Current Liabilities")\
        | Q(ledger_grand_parent = "Current Liabilities")\
            | Q(ledger_parent = "Current Liabilities"),voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0),0)
    try:
        current_ratio = round(current_assets/current_liabilities,2)
        if current_ratio > 2:
            current_ratio_perc = 100
        else:
            current_ratio_perc = round(current_ratio/2,2)
    except:
        current_ratio = 0
        current_ratio_perc = 0
    
    # Cash Ratio #
    cash_equivalent = round(max((Voucher_Ledgers.objects.filter(Q(ledger_primary_group = "Cash-in-hand")\
        | Q(ledger_grand_parent = "Cash-in-hand") | Q(ledger_parent = "Cash-in-hand")\
            | Q(ledger_primary_group = "Bank Accounts") | Q(ledger_grand_parent = "Cash-in-hand") | Q(ledger_parent = "Cash-in-hand"),
            voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'])*-1,0),0)
    try:
        cash_ratio = round(cash_equivalent/current_liabilities,2)
        if cash_ratio > 1:
            cash_ratio_perc = 100
        else:
            cash_ratio_perc = cash_ratio
    except:
        cash_ratio = 0
        cash_ratio_perc = 0
    
    
    return JsonResponse(data={
      'present_income': present_income,
      'previous_income' : previous_income,
      'perc_change_income' : perc_change_income,
      'income_chart_labels' : income_chart_labels,
      'income_chart_data' : income_chart_data,
      'present_expense': present_expense,
      'previous_expense' : previous_expense,
      'perc_change_expense' : perc_change_expense,
      'expense_chart_labels' : expense_chart_labels,
      'expense_chart_data' : expense_chart_data,
      'present_debtor' : present_debtor,
      'present_creditor' : present_creditor,
      'perc_change_debtor' : perc_change_debtor,
      'perc_change_creditor' : perc_change_creditor,
      'recpay_chart_data' : recpay_chart_data,
      'present_cash' : present_cash,
      'perc_change_cash' : perc_change_cash,
      'present_bank' : present_bank,
      'perc_change_bank' : perc_change_bank,
      'cashbank_chart_data' : cashbank_chart_data,
      'present_direct_expense' : present_direct_expense,
      'perc_change_direct_expense' : perc_change_direct_expense,
      'present_gross_profit' : present_gross_profit,
      'perc_change_gross_profit' : perc_change_gross_profit,
      'present_indirect_expense' : present_indirect_expense,
      'perc_change_indirect_expense' : perc_change_indirect_expense,
      'present_net_profit' : present_net_profit,
      'perc_change_net_profit' : perc_change_net_profit,
      'pl_chart_data' : pl_chart_data,
      'top_customer_chart_labels' : top_customer_chart_labels,
      'top_customer_chart_total' : top_customer_chart_total,
      'top_customer_chart_count' : top_customer_chart_count,
      'present_party_receivables' : present_party_receivables,
      'perc_change_party_receivables' : perc_change_party_receivables,
      'top_vendor_chart_labels' : top_vendor_chart_labels,
      'top_vendor_chart_total' : top_vendor_chart_total,
      'top_vendor_chart_count' : top_vendor_chart_count,
      'present_party_payables' : present_party_payables,
      'perc_change_party_payables' : perc_change_party_payables,
      'income_ledgers_chart_labels' : income_ledgers_chart_labels,
      'income_ledgers_chart_data' : income_ledgers_chart_data,
      'perc_change_top_income_ledgers' : perc_change_top_income_ledgers,
      'expense_ledgers_chart_labels' : expense_ledgers_chart_labels,
      'expense_ledgers_chart_data' : expense_ledgers_chart_data,
      'perc_change_top_expense_ledgers' : perc_change_top_expense_ledgers,
      'ageing_labels' : ageing_labels,
      'receivable_ageing_value' : receivable_ageing_value,
      'receivable_ageing_count' : receivable_ageing_count,
      'payable_ageing_value' : payable_ageing_value,
      'payable_ageing_count' : payable_ageing_count,
      'receipts_payments_labels' : receipts_payments_labels,
      'cash_receipts_value' : cash_receipts_value,
      'cash_payments_value' : cash_payments_value,
      'bank_receipts_value' : bank_receipts_value,
      'bank_payments_value' : bank_payments_value,
      'cc_category_chart_labels' : cc_category_chart_labels,
      'cc_category_chart_data' : cc_category_chart_data,
      'perc_change_top_cc_category' : perc_change_top_cc_category,
      'current_ratio' : current_ratio,
      'current_ratio_perc' : current_ratio_perc,
      'cash_ratio' : cash_ratio,
      'cash_ratio_perc' : cash_ratio_perc,
      
    })
    
