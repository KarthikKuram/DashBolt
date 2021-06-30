from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Organization
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ('first_name', 'last_name','email','organization','access')
    list_filter = ('organization','access')
    ordering = ('-date_registered',)
    list_display = ('first_name','last_name','email','organization','access')
    fieldsets = (
        ('Details',{'fields':('first_name','last_name', 'email','organization',)}),('Permission',{'fields':('access','is_active',)}),
        ('Dates',{'fields':('date_registered','validity')})
        )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('first_name','last_name','email','password1','password2','organization','access',)
        }),
    )
    
admin.site.register(User,CustomUserAdmin)
admin.site.register(Organization)