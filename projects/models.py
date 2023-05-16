from django.db import models
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import gettext_lazy as _

PROJECT_DELETED="Project was successfully deleted"

class projects(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    project_po = models.CharField(max_length=5)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_initiated = models.DateField(null=True, blank=True)
    date_updated = models.DateField(auto_now=True)
    company = models.ForeignKey(
        'customers.company', 
        on_delete=models.CASCADE,
    )
    class Status(models.IntegerChoices):
        CREATED = 1, _("Created")
        TESTING = 2, _("Testing")
        COMPLETED = 3, _("Completed")
        CANCELLED = 4, _("Cancelled")
    project_status = models.IntegerField(choices=Status.choices, default =1)
    project_samples = models.ManyToManyField('samples.samples')
    active = models.BooleanField(default=True)

    # methods
    def __str__(self) -> str:
        return self.project_name
    
    def get_allsamples(self) -> list:
        return [sample.sample_name for sample in self.project_samples.all()]

    def is_projectcomplete(self) -> bool:
        samplelist = [sample.sample_status for sample in list(self.project_samples.all())]
        return True if set(samplelist)==set([3]) else False
    
    def get_fields(self) -> list:
        return [(field.name, field.value_to_string(self)) for field in projects._meta.fields]
    
    def get_status(self):
        return self.Status(self.project_status).label

    @classmethod
    def all(cls) -> list:
        return get_list_or_404(projects)
    
    @classmethod 
    def get_projectbyid(cls, id) -> object:
        return get_object_or_404(cls,id=id)
    
    #test
    @classmethod
    def get_projectbycompany(cls, company) -> list:
        return get_list_or_404(cls, company=company)

    @classmethod
    def delete(cls, id) -> None:
        return projects.objects.get(id=id).delete()
    
    # should also have a status: logged in, under testing, reported and archived??
    # should have a tenative TAT date assigned based on samples
    # that takes the longest to complete

    # should have a property to see who set up the project
    # for traceability purposes. Projects that are set up 
    # by 'customers' should auto fill company
class projectForm(ModelForm):
    class Meta:
        model = projects
        fields = ['project_name', 'project_po']