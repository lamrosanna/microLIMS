from django.db import models
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import gettext_lazy as _

from .managers import Sample_TestingManager

# Create your models here.
class test(models.Model):
    id=models.BigAutoField(primary_key=True)
    test_name = models.CharField(max_length=20, unique=True)
    test_code= models.CharField(max_length=10, unique=True)
    testMethod = models.CharField(max_length=20)
    class Tst_type(models.IntegerChoices):
        QUANTITATIVE = 1, _("QUANTITATIVE")
        QUALITATIVE = 2, _("QUALITATIVE")
    test_type=models.IntegerField(
        choices=Tst_type.choices,
        default=1,
    )
    test_TAT= models.IntegerField()
    active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.test_name
    def get_fields(self) -> list:
        return[(field.name, field.value_to_string(self)) for field in test._meta.fields]
    
    def get_type(self):
        return self.Tst_type(self.test_type).label
    @classmethod
    def get_bycode(cls, testcode) -> object:
        return get_object_or_404(cls, test_code=testcode)
    
    @classmethod
    def get_bycompany(cls, companyid) -> list:
        return test.objects.filter(company=companyid)
    
    @classmethod
    def get_byid(cls, id) -> object:
        return get_object_or_404(cls, id=id)
    
    @classmethod
    def get_byname(cls, name) -> object:
        return get_object_or_404(cls, test_name=name)
    
    @classmethod
    def get_all(cls) -> list:
        return test.objects.all()

class testdetailsForm(ModelForm):
    class Meta:
        model = test
        fields=['test_name', 'test_code', 'testMethod', 'test_type', 'test_TAT']

class Sample_Testing(models.Model):
    testing = models.ForeignKey('test_methods.test', on_delete=models.CASCADE)
    sample = models.ForeignKey('samples.samples', on_delete=models.CASCADE)
    class Status(models.IntegerChoices):
        CREATED = 1, _("Created")
        TESTING = 2, _("Testing")
        COMPLETED = 3, _("Completed")
        CANCELLED = 4, _("Cancelled")
    test_status = models.IntegerField(choices=Status.choices, default =1)

    objects = Sample_TestingManager()
    def __str__(self):
        return str(self.test_status)
    def get_status(self):
        return self.Status(self.test_status).label
    @classmethod
    def get_bysample(cls, sample) -> list:
        return get_list_or_404(cls, sample=sample)
    @classmethod
    def get_byid(cls, id) -> object:
        return get_object_or_404(cls, id=id)
    
    @classmethod
    def is_testingcomplete(cls, sample):
        testing = get_list_or_404(cls, sample=sample)
        sampletest=[x.test_status for x in testing]
        if 1 not in sampletest and 2 not in sampletest:
            return True
        return False
    
    @classmethod
    def delete(self, id) -> None:
        return Sample_Testing.objects.filter(id=id).delete()