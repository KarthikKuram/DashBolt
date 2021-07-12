from django.db import models
from .managers import CustomUserManager, Organization
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import CICharField,CIEmailField
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

# Create your models here.

def get_validity():
    return datetime.now() + timedelta(days=15)

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(_('first name'),max_length=30,blank=False)
    last_name = models.CharField(_('last name'),max_length=30,blank=False)
    email = CIEmailField(_('email address'),unique=True)
    organization = models.ForeignKey('users.Organization',on_delete=models.CASCADE,blank=True,related_name='user_organization')
    date_registered = models.DateTimeField(_('date registered'),default= datetime.now)
    validity = models.DateTimeField(_('validity'),default= get_validity)
    access = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email