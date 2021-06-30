from django import forms
from django.forms import widgets
from .models import Tally_Detail

class Tally_Details_Form(forms.ModelForm):
    class Meta:
        model = Tally_Detail
        fields = ('name','tally_begin_date','tally_port',)
        widgets = {
            'tally_begin_date': forms.widgets.DateInput(attrs={'type': 'date'})
            }
