from django.shortcuts import redirect, render

from django.contrib import messages
from django.utils import timezone

from .models import samples
from .forms import SamplesForm
from projects.models import projects
from test_methods.models import Sample_Testing, test

DELETE_SUCCESSFUL="Sample was successfully deleted"
DELETE_FAIL="There was an error in deletiing sample"

def add_sample(request, project_id):
    project = projects.get_projectbyid(id=project_id)
    if request.method == 'POST':
        form = SamplesForm(request.POST)
        if form.is_valid():
            form.instance.sample_project=project            
            sample=form.save()
            messages.success(request, "sample has been created")
            for analysis in sample.analysis.all():
                tests= test.get_byname(analysis)
                test_samples=Sample_Testing(testing=tests, sample=sample)
                test_samples.save()
                messages.success(request, "sample testing has been created")
    sample = samples.objects.filter(sample_project_id=project_id)
    form = SamplesForm()
    context = {'form':form, 'project':project, 'sample':sample}
    return render(request, 'add_sample.html', context)

def modify_sample(request, sample_id, project_id):
    sample = samples.get_byid(id=sample_id)
    form=SamplesForm(instance=sample)
    if request.method == 'POST':
        form=SamplesForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
    project = projects.get_projectbyid(id=project_id)        
    context = {'form':form, 'sample':sample, 'project':project}
    return render(request, 'modify_sample.html', context)

def view_samples(request, project_id):
    project = projects.get_projectbyid(id=project_id)
    sample = samples.get_byproject(project)
    context = {'samples':sample, 'project':project}
    return render(request, 'view_samples.html', context)

def delete_sample(request, sample_id, project_id):

    if samples.delete(id=sample_id):
        messages.success(request, DELETE_SUCCESSFUL)
        project = projects.get_projectbyid(project_id)
        return redirect('view_project', project_id=project.id)
    else:
        messages.error(request, DELETE_FAIL)
    project = projects.get_projectbyid(project_id)
    sample = samples.get_byproject(project)
    print(sample)
    context = {'project':project, 'sample':sample}
    return render(request, 'view_project.html', context)

def initiate_testing(request, sample_id):
    initiate_sampletesting = samples.get_byid(id = sample_id)
    project = projects.get_projectbyid(initiate_sampletesting.project.id)
    if initiate_sampletesting.sample_status == 1:
        initiate_sampletesting.sample_status =2
        initiate_sampletesting.testing_started = timezone.now
        initiate_sampletesting.save()
    if project.status == 1:
        project.status = 2
        project.save()
    context = {'project':project, 'samples':initiate_sampletesting}
    return render(request, 'view_project.html', context)
