from django.db import models
from django.db.models.enums import Choices
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

# Create your models here.
class test(models.Model):
    id=models.BigAutoField(primary_key=True)
    test_name = models.CharField(max_length=20)
    test_code= models.CharField(max_length=10, unique=True)
    testMethod = models.CharField(max_length=20)
    class Tst_type(models.IntegerChoices):
        QUANTITATIVE = 1
        QUALITATIVE = 2
    test_type=models.IntegerField(
        choices=Tst_type.choices,
        default=1,
    )
    test_TAT= models.IntegerField()
    completed = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.test_name
    def get_fields(self) -> list:
        return[(field.name, field.value_to_string(self)) for field in test._meta.fields]
    
    @classmethod
    def get_bycode(cls, testcode) -> object:
        return get_object_or_404(cls, test_code=testcode)

class testdetailsForm(ModelForm):
    class Meta:
        model = test
        fields=['test_name', 'test_code', 'testMethod', 'test_type', 'test_TAT']