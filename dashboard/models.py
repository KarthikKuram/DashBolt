from django.db import models
from users.models import User

# Create your models here.
class Tally_Detail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tally_begin_date = models.DateField()
    tally_port = models.IntegerField(default=9000)
    organization = models.ForeignKey('users.Organization', related_name='tally_organization',on_delete=models.CASCADE,blank=True)
    account_id = models.EmailField(max_length=254,help_text="Registered AccountID of Tally")
    computer_name = models.CharField(max_length=255,help_text="Name of the computer where tdl and tally is running. Please see system settings to get computer name.")
    
    class Meta:
        verbose_name = 'Tally Detail'
        verbose_name_plural = 'Tally Details'
        unique_together = ('name', 'account_id',)
    
    def __str__(self):
        return self.name
    
class Ledger_Category(models.Model):
    CATEGORY_CHOICES = (
        ('Asset', 'Asset'),
        ('Liability','Liability'),
        ('Income','Income'),
        ('Expense','Expense')
        )
    primary_group = models.CharField(max_length=255)
    category = models.CharField(max_length=255,choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name = 'Ledger Category'
        verbose_name_plural = 'Ledger Categories'
        
    def __str__(self):
        return '%s - %s' %(self.primary_group,self.category)
    
class Ledger_Master(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    category = models.CharField(max_length=255,null=True)
    primary_group = models.CharField(max_length=255,null=True)
    grand_parent = models.CharField(max_length=255,null=True)
    parent = models.CharField(max_length=255,null=True)
    ledger = models.CharField(max_length=255,null=False)
    opening_balance = models.FloatField(default=0,null=True)
    closing_balance = models.FloatField(default=0,null=True)
    company = models.CharField(max_length=255)
    class Meta:
        verbose_name = 'Ledger Master'
        verbose_name_plural = 'Ledger Masters'
        
    def __str__(self):
        return '%s-%s-%s' %(self.grand_parent, self.parent,self.ledger)
    
class VoucherTypes(models.Model):
    alter_id = models.IntegerField()
    name = models.CharField(max_length=50)
    parent = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    company = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Voucher Type"
        verbose_name_plural = "Voucher Types"
        
    def __str__(self):
        return self.name    
    
class Voucher_Details(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    voucher_key = models.CharField(max_length=255)
    voucher_number = models.CharField(max_length=255)
    date = models.DateField()
    voucher_type = models.CharField(max_length=255)
    voucher_view = models.CharField(max_length=255)
    create_date = models.DateField()
    create_time = models.TimeField()
    alter_date = models.DateField()
    alter_time = models.TimeField()
    narrations = models.CharField(max_length=500,null=True)
    company = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Voucher Detail'
        verbose_name_plural = 'Voucher Details'
        
    def __str__(self):
        return '%s - %s' %(self.voucher_number,self.date.strftime('%m-%b-%Y'))

class IncomeManager(models.Manager):
    def get_queryset(self):
        return super(IncomeManager, self).get_queryset().filter(ledger_category='Income')    
class ExpenseManager(models.Manager):
    def get_queryset(self):
        return super(ExpenseManager, self).get_queryset().filter(ledger_category='Expense')
class DebtorManager(models.Manager):
    def get_queryset(self):
        return super(DebtorManager, self).get_queryset().filter(ledger_primary_group='Sundry Debtors')
    
class CreditorManager(models.Manager):
    def get_queryset(self):
        return super(CreditorManager, self).get_queryset().filter(ledger_primary_group='Sundry Creditors')
class CashManager(models.Manager):
    def get_queryset(self):
        return super(CashManager, self).get_queryset().filter(ledger_primary_group='Cash-in-hand')
class BankManager(models.Manager):
    def get_queryset(self):
        return super(BankManager, self).get_queryset().filter(ledger_primary_group='Bank Accounts')

class Voucher_Ledgers(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    voucher_key = models.CharField(max_length=255)
    voucher_number = models.CharField(max_length=255)
    voucher_date = models.DateField()
    ledger = models.CharField(max_length=255)
    amount = models.FloatField()
    ledger_master_id = models.IntegerField()
    ledger_alter_id = models.IntegerField()
    ledger_category = models.CharField(max_length=255,null=True)
    ledger_primary_group = models.CharField(max_length=255,null=True)
    ledger_grand_parent = models.CharField(max_length=255,null=True)
    ledger_parent = models.CharField(max_length=255,null=True)
    company = models.CharField(max_length=255)
    objects = models.Manager()
    income = IncomeManager()
    expense = ExpenseManager()
    debtor = DebtorManager()
    creditor = CreditorManager()
    cash = CashManager()
    bank = BankManager()
    
    class Meta:
        verbose_name = 'Voucher Ledger'
        verbose_name_plural = 'Voucher Ledgers'
        
    def __str__(self):
        return '%s - %s - %s' %(self.voucher_date.strftime('%m-%b-%Y'),self.voucher_number,self.ledger)   
class Voucher_Bills(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    voucher_key = models.CharField(max_length=255)
    voucher_number = models.CharField(max_length=255)
    voucher_date = models.DateField()
    ledger = models.CharField(max_length=255)
    ledger_master_id = models.IntegerField()
    ledger_alter_id = models.IntegerField()
    ledger_category = models.CharField(max_length=255,null=True)
    ledger_primary_group = models.CharField(max_length=255,null=True)
    ledger_grand_parent = models.CharField(max_length=255,null=True)
    ledger_parent = models.CharField(max_length=255,null=True)
    bill_name = models.CharField(max_length=255,null=True)
    bill_type = models.CharField(max_length=255,null=True)
    bill_amount = models.FloatField()
    company = models.CharField(max_length=255)
    class Meta:
        verbose_name = 'Voucher Bill'
        verbose_name_plural = 'Voucher Bills'
        
    def __str__(self):
        return '%s - %s - %s - %s' %(self.voucher_date.strftime('%m-%b-%Y'),self.voucher_number,self.ledger,self.bill_name)
class Voucher_CostCenters(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    voucher_key = models.CharField(max_length=255)
    voucher_number = models.CharField(max_length=255)
    voucher_date = models.DateField()
    ledger = models.CharField(max_length=255)
    ledger_master_id = models.IntegerField()
    ledger_alter_id = models.IntegerField()
    ledger_category = models.CharField(max_length=255,null=True)
    ledger_primary_group = models.CharField(max_length=255,null=True)
    ledger_grand_parent = models.CharField(max_length=255,null=True)
    ledger_parent = models.CharField(max_length=255,null=True)
    cc_category = models.CharField(max_length=255,null=True)
    cc_name = models.CharField(max_length=255,null=True)
    cc_amount = models.FloatField()
    company = models.CharField(max_length=255)
    class Meta:
        verbose_name = 'Voucher CostCenter'
        verbose_name_plural = 'Voucher CostCenters'
        
    def __str__(self):
        return '%s - %s - %s - %s' %(self.voucher_date.strftime('%m-%b-%Y'),self.voucher_number,self.ledger,self.cc_name)
class Voucher_BankDetails(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    voucher_key = models.CharField(max_length=255)
    voucher_number = models.CharField(max_length=255)
    voucher_date = models.DateField()
    ledger = models.CharField(max_length=255)
    ledger_master_id = models.IntegerField()
    ledger_alter_id = models.IntegerField()
    ledger_category = models.CharField(max_length=255,null=True)
    ledger_primary_group = models.CharField(max_length=255,null=True)
    ledger_grand_parent = models.CharField(max_length=255,null=True)
    ledger_parent = models.CharField(max_length=255,null=True)
    bank_date = models.DateField(null=True)
    transaction_type = models.CharField(max_length=255,null=True)
    instrument_number = models.CharField(max_length=255,null=True)
    instrument_amount = models.FloatField()
    company = models.CharField(max_length=255)
    class Meta:
        verbose_name = 'Voucher BankDetail'
        verbose_name_plural = 'Voucher BankDetails'
        
    def __str__(self):
        return '%s - %s - %s - %s' %(self.voucher_date.strftime('%m-%b-%Y'),self.voucher_number,self.ledger,self.instrument_number)