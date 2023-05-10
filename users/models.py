from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.shortcuts import get_list_or_404
from .managers import CustomUserManager

class LIMSuser(AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey(
        'customers.company',
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=12)
    email= models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects= CustomUserManager()

    def __str__(self):
        return self.email
    
    @classmethod
    def get_bycompany(cls, company) -> list:
        return get_list_or_404(cls, company=company)



