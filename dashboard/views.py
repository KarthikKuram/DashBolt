from django.views.generic import CreateView,UpdateView,RedirectView,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError, Sum, Q, Count,Min,Case,Value,When,FloatField,DateField,ExpressionWrapper,F,IntegerField,CharField
from django.db.models.functions import Cast,ExtractDay,TruncDate
from .forms import Tally_Details_Form
from .models import Tally_Detail,Voucher_Ledgers,Ledger_Master,Voucher_Bills
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
            income_chart_data.append(float(entry['total']))          
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
            expense_chart_data.append(float(entry['total'])*-1)          
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
    debtor_bills_ref = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors").exclude(bill_type = "On Account").\
        values('bill_name').annotate(
            bill_date = Min('voucher_date'),
            net_due = Sum('bill_amount')*-1,
            cutoff_date = Value(end_date_pd,output_field=DateField()),
            age=Cast(ExtractDay(TruncDate(F('cutoff_date')) - TruncDate(F('bill_date'))),output_field = IntegerField()),
            age_group = Case(
                        When(age__range = [0,30],then = Value('0-30')),
                        When(age__range = [31,60],then = Value('31-60')),
                        When(age__range = [61,90],then = Value('61-90')),
                        When(age__range = [91,120],then = Value('91-120')),
                        When(age__gt = 120,then = Value('>>120')),
                        default = Value('No Group'),
                        output_field = CharField()
                    )
            ).filter(net_due__gt = 0).values_list('age_group','net_due')
    debtor_bills_ref = pd.DataFrame(debtor_bills_ref,columns = ['Age_Group','Due'])
    debtor_bills_ref = debtor_bills_ref.groupby('Age_Group').Due.agg(['sum','count'])
    
    debtor_bills_onaccount = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors",bill_type = "On Account").\
        values('bill_name').annotate(net_due = Sum('bill_amount')*-1, count = Count('bill_amount')).\
            filter(net_due__gt = 0).values_list('net_due','count')
            
    if debtor_bills_onaccount.exists():
        print("Yes")
    else:
        print("No")            
        
        
    # debtor_bills = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors").exclude(bill_type = "On Account").\
    #     values('bill_name').annotate(
    #         bill_date = Min('voucher_date'),
    #         net_due = Sum('bill_amount')*-1,
    #         cutoff_date = Value(end_date_pd,output_field=DateField()),
    #         age=Cast(ExtractDay(TruncDate(F('cutoff_date')) - TruncDate(F('bill_date'))),output_field = IntegerField())).\
    #             filter(net_due__gt = 0).annotate(
    #                 age_group = Case(
    #                     When(age__range=[0,30],then= Value('0-30')),
    #                     When(age__range=[31,60],then= Value('31-60')),
    #                     When(age__range=[61,90],then= Value('61-90')),
    #                     When(age__range=[91,120],then= Value('91-120')),
    #                     When(age__gt=120,then= Value('>>120')),
    #                     default = Value('No Group'),
    #                     output_field = CharField()
    #                 )
    #             ).values('age_group').annotate(total=Sum(F('net_due')))
    
    # debtor_bills = Voucher_Bills.objects.filter(voucher_date__lte=end_date,ledger_primary_group="Sundry Debtors").exclude(bill_type = "On Account").\
    #     values('bill_name').annotate(
    #         Booking_Date = Case(
    #         When(bill_amount__lt = 0, then = Min('voucher_date')),
    #         output_field = DateField()
    #     ),
    #         Booked_Amount = Case(
    #         When(bill_amount__lt = 0,then = Sum('bill_amount')*-1),
    #         default = 0,output_field=FloatField()
    #     ),
    #         Paid_Amount = Case(
    #             When(bill_amount__gt = 0, then = Sum('bill_amount')),
    #             default = 0, output_field = FloatField()
    #                                  )).filter(bill_name = '0082/2019-20')
    # print(debtor_bills_ref)
        
    ### CASH & BANK DASH CARD ###
    cashbank_chart_data = []
    try:
        present_cash = round(Voucher_Ledgers.cash.filter(voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1        
        cashbank_chart_data.append(float(present_cash))
    except:
        present_cash = 0
        cashbank_chart_data.append(float(present_cash))
    try:
        previous_cash = round(Voucher_Ledgers.cash.filter(voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
    except:
        previous_cash = 0
    try:
        present_bank = round(Voucher_Ledgers.bank.filter(voucher_date__range=[start_date,end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
        cashbank_chart_data.append(float(present_bank))
    except:
        present_bank = 0
        cashbank_chart_data.append(float(present_bank))
    try:
        previous_bank = round(Voucher_Ledgers.bank.filter(voucher_date__range=[previous_start_date,previous_end_date]).aggregate(Sum('amount'))['amount__sum'],0)*-1
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
    
    
    ### FINDING NUMBER OF DIGITS OF VARIOUS FIGURES FOR DISPLAY IN DASHBOARD ###
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
        
    digits = find_digits(present_debtor)
    if digits > 6:
        present_debtor = round(present_debtor/100000,2)
        present_debtor_denomination = " L"
    else:
        present_debtor_denomination = ""                
    
    digits = find_digits(present_creditor)
    if digits > 6:
        present_creditor = round(present_creditor/100000,2)
        present_creditor_denomination = " L"
    else:
        present_creditor_denomination = ""                    
        
    digits = find_digits(present_cash)
    if digits > 6:
        present_cash = round(present_cash/100000,2)
        present_cash_denomination = " L"
    else:
        present_cash_denomination = ""                
    
    digits = find_digits(present_bank)
    if digits > 6:
        present_bank = round(present_bank/100000,2)
        present_bank_denomination = " L"
    else:
        present_bank_denomination = ""                    
    
    digits = find_digits(present_direct_expense)
    if digits > 6:
        present_direct_expense = round(present_direct_expense/100000,2)
        present_direct_expense_denomination = " L"
    else:
        present_direct_expense_denomination = ""
    
    digits = find_digits(present_gross_profit)
    if digits > 6:
        present_gross_profit = round(present_gross_profit/100000,2)
        present_gross_profit_denomination = " L"
    else:
        present_gross_profit_denomination = ""    
    
    digits = find_digits(present_indirect_expense)
    if digits > 6:
        present_indirect_expense = round(present_indirect_expense/100000,2)
        present_indirect_expense_denomination = " L"
    else:
        present_indirect_expense_denomination = ""
    
    digits = find_digits(present_net_profit)
    if digits > 6:
        present_net_profit = round(present_net_profit/100000,2)
        present_net_profit_denomination = " L"
    else:
        present_net_profit_denomination = ""
       
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
      'present_debtor' : present_debtor,
      'present_debtor_denomination' : present_debtor_denomination,
      'present_creditor' : present_creditor,
      'present_creditor_denomination' : present_creditor_denomination,
      'perc_change_debtor' : perc_change_debtor,
      'perc_change_creditor' : perc_change_creditor,
      'recpay_chart_data' : recpay_chart_data,
      'present_cash' : present_cash,
      'present_cash_denomination' : present_cash_denomination,
      'perc_change_cash' : perc_change_cash,
      'present_bank' : present_bank,
      'present_bank_denomination' : present_bank_denomination,
      'perc_change_bank' : perc_change_bank,
      'cashbank_chart_data' : cashbank_chart_data,
      'present_direct_expense' : present_direct_expense,
      'present_direct_expense_denomination' : present_direct_expense_denomination,
      'perc_change_direct_expense' : perc_change_direct_expense,
      'present_gross_profit' : present_gross_profit,
      'present_gross_profit_denomination' : present_gross_profit_denomination,
      'perc_change_gross_profit' : perc_change_gross_profit,
      'present_indirect_expense' : present_indirect_expense,
      'present_indirect_expense_denomination' : present_indirect_expense_denomination,
      'perc_change_indirect_expense' : perc_change_indirect_expense,
      'present_net_profit' : present_net_profit,
      'present_net_profit_denomination' : present_net_profit_denomination,
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
      
    })
    