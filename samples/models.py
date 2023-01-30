from django.db import models
from django.forms import ModelForm
# Create your models here.

class samples(models.Model):
    sample_name = models.CharField(max_length=15)
    sample_description = models.CharField(max_length=100)
    sample_created = models.DateTimeField(auto_created=True)
    analysis = models.ManyToManyField('test_methods.test')

class sampleForm(ModelForm):
    class Meta:
        model = samples
        fields='__all__'