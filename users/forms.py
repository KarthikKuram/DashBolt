from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import User, Organization
from django import forms
from betterforms.multiform import MultiModelForm

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','organization',)
        
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
        
class RegisterForm(MultiModelForm):
    form_classes = {
        'user': NewUserForm,
        'organization': OrganizationForm,
    }        