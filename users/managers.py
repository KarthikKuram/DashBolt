from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255,unique=False)
    
    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self,email, password, **extra_fields):
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('access',False)
        extra_fields.setdefault('org_admin',False)
        return self._create_user(email, password, **extra_fields)
    
    
    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('access',True)
        extra_fields.setdefault('org_admin',True)
        organization = Organization(
            name = "Optimalytics Business Solutions Private Limited"
        )
        organization.save()
        extra_fields.setdefault('organization',organization)
            
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True'))
        
        if extra_fields.get('access') is not True:
            raise ValueError(_('Superuser must have access=True'))
        
        if extra_fields.get('org_admin') is not True:
            raise ValueError(_('Superuser must have org_admin=True'))
        
        return self._create_user(email, password, **extra_fields)
        
            