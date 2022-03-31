from django import forms
from django.forms import widgets
from .models import Tally_Detail
from users.models import User


class Tally_Details_Form(forms.ModelForm):
    class Meta:
        model = Tally_Detail
        fields = ('name','tally_begin_date','tally_port','account_id','computer_name',)
        widgets = {
            'tally_begin_date': forms.widgets.DateInput(attrs={'type': 'date'})
            }

class Tally_Valid_Users_Form(forms.ModelForm):
    
    def __init__(self, user,*args, **kwargs):
        super(Tally_Valid_Users_Form,self).__init__(*args,**kwargs)
        self.fields['valid_users'].queryset = User.objects.filter(
            organization = user.organization
        )
        instance = getattr(self,'instance',None)
        if instance and instance.pk:
            self.fields['name'].disabled = True
            
    class Meta:
        model = Tally_Detail
        fields = ('name','valid_users',)
        
    valid_users = forms.ModelMultipleChoiceField(
        queryset= None,
        widget = forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"})
    )