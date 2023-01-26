from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class LIMSuser(models.Model):
    company = models.ForeignKey(
        'customers.company',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=12)
    email= models.EmailField()


class LIMSuserForm(ModelForm):
    class Meta:
        model = LIMSuser
        fields='__all__'
