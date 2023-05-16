from django.db import models
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, get_list_or_404

from projects.models import projects

# Error Msg 
SAMPLE_DELETED="Sample deleted"

class samples(models.Model):
    id = models.BigAutoField(primary_key=True)
    sample_name = models.CharField(max_length=15)
    sample_description = models.CharField(max_length=100)
    sample_created = models.DateTimeField(auto_now_add=True, blank=True)
    analysis = models.ManyToManyField('test_methods.test')
    sample_project = models.ForeignKey(projects, on_delete=models.CASCADE)
    testing_started=models.DateField(null=True, blank=True)
    testing_completed=models.DateField(null=True, blank=True)
    class Status(models.IntegerChoices):
        CREATED = 1
        TESTING = 2
        COMPLETED = 3
        CANCELLED = 4
    sample_status= models.IntegerField(choices=Status.choices, default=1)
    active = models.BooleanField(default=True)

    # methods
    def __str__(cls) -> str:
            return cls.sample_name
    
    @classmethod
    def get(cls, name) -> object:
        return get_object_or_404(cls, sample_name=name)
        #cls.save()
    
    @classmethod
    def get_byid(cls, id) -> object:
        return get_object_or_404(cls, id=id)
    
    @classmethod
    def get_byproject(cls, project) -> list:
        return samples.objects.filter(sample_project=project)
    
    @classmethod
    def get_allsamples(cls) -> list:
        return samples.objects.all()
    
    @classmethod
    def delete(cls, id) -> None:
        return samples.objects.filter(id=id).delete()
        
    def get_allanalysis(self) -> list:
        return [x.test_name for x in list(self.analysis.all())]

    def get_latestTat(self) -> int:
        tat_list = [x.test_TAT for x in list(self.analysis.all())]
        return max(tat_list)
    
    def is_testingfinished(self) -> bool:
        testlist = [x.completed for x in list(self.analysis.all())]
        return False if False in testlist else True
    