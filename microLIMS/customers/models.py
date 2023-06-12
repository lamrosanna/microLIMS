from typing import Any, Dict, Tuple
from django.db import models
from django.db.models.enums import Choices
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404

# Create your models here.
class company(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=200)
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'/")
    phone= models.CharField(validators=[phone_regex], max_length=16, blank=True,default='999999999') # validators should be a list
    active=models.BooleanField(default=True)
    CUSTOMER='Customer'
    INTERNAL='Internal'
    EN_type=[
        ('CUSTOMER','Customer'),
        ('INTERNAL','Internal'),
        ]
    entity= models.CharField(
        max_length=9,
        choices=EN_type,
        default=CUSTOMER,
    )
    class Meta:
        app_label='customers'
    def __str__(self) -> str:
        return self.company_name
    
    def get_fields(self) -> list:
        return[(field.name, field.value_to_string(self)) for field in company._meta.fields]

    @classmethod
    def get_byid(cls, id) -> object:
        return get_object_or_404(cls, id=id)
    
    def delete(self, id):
        return company.objects.get(id=id).delete()
    
class companyForm(ModelForm):
    class Meta:
        model = company
        exclude=["entity","active"]



