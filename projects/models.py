from django.db import models
from django.forms import ModelForm
# Create your models here.


class projects(models.Model):
    project_name = models.CharField(max_length=200)
    project_po = models.CharField(max_length=5)
    date_submitted = models.DateTimeField(auto_created=True)
    date_initiated = models.DateField(auto_created=False)
    date_updated = models.DateField(auto_now=True)
    company = models.ForeignKey(
        'customers.company', 
        on_delete=models.CASCADE,
    )

class projectForm(ModelForm):
    class Meta:
        model = projects
        exclude = ['company']