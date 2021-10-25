from django.db import models
from django.db.models.enums import Choices
from django.forms import ModelForm

# Create your models here.
class test(models.Model):
    test_name = models.CharField(max_length=20)
    test_code= models.CharField(max_length=10)
    testMethod = models.CharField(max_length=20)
    QUANTITATIVE='Quantitative'
    QUALITATIVE='Qualitative'
    tst_type=[
        ('QUANTITATIVE','Quantitative'),
        ('QUALITATIVE','Qualitative'),
    ]
    test_type=models.CharField(
        max_length=12,
        choices=tst_type,
        default=QUALITATIVE,
    )
    def __str__(self):
        return self.name
    def get_fields(self):
        return[(field.name, field.value_to_string(self)) for field in test._meta.fields]

class testdetailsForm(ModelForm):
    class Meta:
        model = test
        fields='__all__'