from django.shortcuts import redirect, render
from django.contrib import messages
import datetime

from .models import samples
from .forms import SamplesForm
from projects.models import projects
from test_methods.models import Sample_Testing, test

DELETE_SUCCESSFUL="Sample was successfully deleted"
DELETE_FAIL="There was an error in deletiing sample"
INITIATE_TESTING_ERROR="There was an error in initiating testing"
INITIATE_TESTING_SUCCESS="Testing has been initiated"
SAMPLE_IN_TEST="Unable to delete, Sample is in testing"

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
    active_sample=samples.get_byid(id=sample_id)
    if active_sample.sample_status == 1:
        if samples.delete(id=sample_id):
            messages.success(request, DELETE_SUCCESSFUL)
            project = projects.get_projectbyid(project_id)
            return redirect('view_project', project_id=project.id)
        else:
            messages.error(request, DELETE_FAIL)
    else:
        messages.error(request, SAMPLE_IN_TEST)
    project = projects.get_projectbyid(project_id)
    sample = samples.get_byproject(project)
    print(sample)
    context = {'project':project, 'sample':sample}
    return render(request, 'view_project.html', context)

def initiate_testing(request, project_id, sampletesting_id):
    track_test=Sample_Testing.get_byid(id=sampletesting_id)
    project = projects.get_projectbyid(id=project_id)
    sampletesting = samples.get_byid(id=track_test.sample.id)
    if track_test.test_status == 1:
        if sampletesting.sample_status == 1:
            sampletesting.sample_status = 2
            sampletesting.testing_started = datetime.datetime.today()
            sampletesting.save()
        if project.project_status == 1:
            project.status = 2
            project.save()
        track_test.test_status = 2
        track_test.save()
        if project.project_status == 2 & sampletesting.sample_status==2 & track_test.test_status==2:
            sample = samples.get_byproject(project)
            sample_tests=Sample_Testing.objects.all()
            messages.success(request, INITIATE_TESTING_SUCCESS)
        return redirect('view_project', project_id=project.id)  
    else:
        messages.error(request, INITIATE_TESTING_ERROR)
        sample = samples.get_byproject(project)
        sample_tests=Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html', context)

def complete_testing(request, project_id, sampletesting_id):
    track_test=Sample_Testing.get_byid(id=sampletesting_id)
    project = projects.get_projectbyid(id=project_id)
    sampletesting = samples.get_byid(id=track_test.sample.id)
    if track_test.test_status == 2:
        track_test.test_status = 3
        track_test.save()
        sample_complete = Sample_Testing.is_testingcomplete(sampletesting)
        if sample_complete:
            sampletesting.sample_status = 3
            sampletesting.testing_completed = datetime.datetime.today()
            sampletesting.save()
        project_complete = project.is_complete()
        if project_complete:
            project.project_status = 3
            project.save()
        return redirect('view_project', project_id=project.id)
    else:
        messages.error(request,"")
        sample = samples.get_byproject(project)
        sample_tests=Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html', context)

def cancel_sample(request, project_id, sampletesting_id):
    pass