from django import forms

from samples.models import samples
from test_methods.models import test



class SamplesForm(forms.ModelForm):
    class Meta:
        model = samples
        fields=['sample_name', 'sample_description', 'analysis']

    analysis=forms.ModelMultipleChoiceField(
        queryset=test.objects.all(), 
        widget=forms.CheckboxSelectMultiple                                    
        )
    def customSave(self, project):
        self.sample_project=project
        sample=self.save()
        return sample
