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
        unique_together = ('name', 'account_id',)
    
    def __str__(self):
        return self.name
    
class Ledger_Master(models.Model):
    master_id = models.IntegerField()
    alter_id = models.IntegerField()
    primary_group = models.CharField(max_length=255,null=True)
    grand_parent = models.CharField(max_length=255,null=True)
    parent = models.CharField(max_length=255,null=True)
    ledger = models.CharField(max_length=255,null=False)
    opening_balance = models.FloatField(default=0,null=True)
    closing_balance = models.FloatField(default=0,null=True)
    
    
    class Meta:
        verbose_name = 'Ledger_Master'
        verbose_name_plural = 'Ledger_Masters'
        
    def __str__(self):
        return '%s-%s-%s' %(self.grand_parent, self.parent,self.ledger)