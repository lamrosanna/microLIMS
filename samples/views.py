from django.shortcuts import redirect, render
from django.contrib import messages
import datetime

from .models import samples
from .forms import SamplesForm
from projects.models import projects
from test_methods.models import Sample_Testing, test
from test_methods.views import cancel_alltesting, create_sampletesting, initiate_trackingtesting, complete_tracktesting

DELETE_SUCCESSFUL="Sample was successfully deleted"
DELETE_FAIL="There was an error in deletiing sample"
INITIATE_TESTING_ERROR="There was an error in initiating testing"
INITIATE_TESTING_SUCCESS="Testing has been initiated"
SAMPLE_IN_TEST="Unable to delete, Sample is in testing"
ERROR_CANCELLING="There was an error in cancelling sample."
SAMPLE_EXISTS="A sample with the same details already has been created for this project"
UPDATE_ERROR="There was an error updating status of tests"

# create sample
def add_sample(request, project_id):
    project = projects.get_projectbyid(id=project_id)
    if request.method == 'POST':
        form = SamplesForm(request.POST)
        if form.is_valid():
            form.instance.sample_project=project   
            samplename = request.POST.get('sample_name') 
            print(samplename)
            if samples.objects.filter(sample_name=samplename, sample_project=project).exists():
                print("error1")
                messages.error(request, SAMPLE_EXISTS)
                return redirect('add_sample', project_id=project.id)
            else:        
                print("error2")
                sample=form.save()
                create_sampletesting(sample.id)
                add_project(sample_id=sample.id, project_id=project.id)
                messages.success(request, "sample testing has been created")
                return redirect('add_sample', project_id=project.id)
    sample = samples.objects.filter(sample_project_id=project_id)
    form = SamplesForm()
    context = {'form':form, 'project':project, 'sample':sample}
    return render(request, 'add_sample.html', context)

# add sample to object
def add_project(sample_id, project_id):
    sample = samples.get_byid(id=sample_id)
    project = projects.get_projectbyid(id=project_id)
    project.project_samples.add(sample)

# modify sample details
def modify_sample(request, sample_id, project_id):
    sample = samples.get_byid(id=sample_id)
    project = projects.get_projectbyid(id=project_id)
    form = SamplesForm(instance=sample)
    if request.method == 'POST':
        form=SamplesForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
    context = {'form':form, 'sample':sample, 'project':project}
    return render(request, 'modify_sample.html', context)

# view samples by project id
def view_samples(request, project_id):
    project = projects.get_projectbyid(id=project_id)
    sample = samples.get_byproject(project)
    context = {'samples':sample, 'project':project}
    return render(request, 'view_samples.html', context)

#delete sample by sample id
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

# update sample testing status on initiate testing(2):
def initiate_sample(sample_id):
    sample= samples.get_byid(id=sample_id)
    if sample.sample_status == 1:
        sample.sample_status = 2
        sample.testing_started = datetime.datetime.today()
        sample.save()
    return sample

# update sample testing status on completed testing(3):
def complete_sample(sample_id):
    sample = samples.get_byid(id=sample_id)
    if Sample_Testing.is_testingcomplete(sample):
        sample.sample_status = 3
        sample.testing_completed = datetime.datetime.today()
        sample.save()
    return sample

# update sample testing status to cancel(4)
def cancel_sampleid(sample_id):
    sample = samples.get_byid(id=sample_id)
    sample.sample_status = 4
    sample.save() 
    cancel_alltesting(sample_id)
        
# Cancel sample and all related tests 
def cancel_sample(request, project_id, sample_id):
    sample = samples.get_byid(id=sample_id)
    project = projects.get_projectbyid(id=project_id)
    try:
        cancel_sampleid(sample.id)
        cancel_alltesting(sample_id)
        return redirect('view_project', project_id=project.id)
    except:
        messages.error(request, ERROR_CANCELLING)
        sample = samples.get_byproject(project)
        sample_tests=Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html', context)        