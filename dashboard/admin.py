from django.contrib import admin
from .models import Tally_Detail, Ledger_Master, Ledger_Category, Voucher_Details, Voucher_Ledgers, Voucher_Bills, Voucher_CostCenters, Voucher_BankDetails

# Register your models here.
admin.site.register(Tally_Detail)
admin.site.register(Ledger_Category)
admin.site.register(Voucher_Details)
admin.site.register(Voucher_Ledgers)
admin.site.register(Voucher_Bills)
admin.site.register(Voucher_CostCenters)
admin.site.register(Voucher_BankDetails)
