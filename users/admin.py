from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Organization
from django.forms import CheckboxSelectMultiple
from django.db import models
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ('first_name', 'last_name','email','organization','access','org_admin')
    list_filter = ('organization','access','org_admin')
    ordering = ('-date_registered',)
    list_display = ('first_name','last_name','email','organization','access','org_admin')
    fieldsets = (
        ('Details',{'fields':('first_name','last_name', 'email','organization',)}),('Permission',{'fields':('access','org_admin','is_active',)}),
        ('Dates',{'fields':('date_registered','validity')})
        )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('first_name','last_name','email','password1','password2','organization','access','org_admin')
        }),
    )
    
admin.site.register(User,CustomUserAdmin)
admin.site.register(Organization)