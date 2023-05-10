from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from pprint import pprint

from .models import sampleForm, samples
from projects.models import projects

def add_sample(request, project_id):
    project=projects.get_projectbyid(id=project_id)
    print(project)
    check = reverse(add_sample, args=[project_id])
    print(check)
    if request.method == 'POST':
        form = sampleForm(request.POST)
        if form.is_valid():
            form.instance.sample_project = project
            form.save()
    sample = samples.objects.filter(sample_project_id=project_id)
    form= sampleForm()
    context= {'form': form, 'project':project, 'sample':sample}
    return render(request, 'add_sample.html', context)
