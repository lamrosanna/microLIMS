from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Count
import datetime

from .models import projectForm, projects
from samples.models import samples
from samples.views import cancel_sampleid, complete_sample, initiate_sample
from customers.models import company
from test_methods.models import Sample_Testing
from test_methods.views import initiate_trackingtesting, complete_tracktesting

DELETE_SUCCESSFUL="Project was successfully deleted."
DELETE_FAIL="There was an error in deleting project."
PROJECT_EXISTS="Project already exists for company."
PROJECT_CREATED="Project was created successfully."
INACTIVE_PROJECT="The project you are trying to view is inactive. Please contact admin for assistance."
CANCEL_SUCCESS="Project was cancelled."
CANCEL_ERROR="There was an error in cancelling project"
INITIATE_TESTING_ERROR="There was an error in initiating testing"
INITIATE_TESTING_SUCCESS="Testing has been initiated"
UPDATE_ERROR="There was an error updating status of tests"

#generate date as string for project name
def gen_name():
    day = datetime.datetime.today()
    date = day.strftime("%m%d%Y")
    return date

# Home page 
@login_required
def home(request):
    project = projects.objects.filter(active=True).order_by('project_status')
    context={"project":project}
    return render(request, 'index.html', context)

# add projects 
def add_project(request):
    if request.method == 'POST':
        form = projectForm(request.POST)
        if form.is_valid():
            project_company=request.POST.get('company')
            project_name = request.POST.get('project_name')
            if projects.objects.filter(project_name=project_name, company=project_company).exists():
                messages.error(request, PROJECT_EXISTS)
            else:
                project = form.save()
                return redirect('view_project', project_id=project.id)
    form = projectForm()
    project = projects.objects.all()
    context= {'form':form, 'project':project}
    return render(request, 'add_projects.html', context)

# view projects by id 
def view_project(request, project_id):
    project = projects.get_projectbyid(project_id)
    if project.is_active():
        sample = samples.get_byproject(project_id)
        sample_tests=Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html',context)
    else:
        messages.error(request, INACTIVE_PROJECT)
        return redirect('/')

# view all active projects by company(companyid)
def view_allproject(request, company_id):
    companyProject = company.get_byid(id=company_id)
    project = projects.objects.filter(company=company_id).filter(active=True)
    context = {'project':project, 'company':companyProject}
    return render(request, 'all_projects.html', context)

# view all currently active projects 
def all_activeprojects(request):
    allprojects = projects.objects.filter(active=True)
    # allprojects.
    # samplecount = projects.objects.annotate(count=Count('project_samples'))
    context={'project':allprojects}
    return render(request, 'all_activeprojects.html', context)

# modify project by id
def modify_project(request, project_id):
    project=projects.get_projectbyid(id=project_id)
    if project.is_active():
        form = projectForm(instance=project)
        if request.method == 'POST':
            form = projectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
        context={'form':form, 'project':project}
        return render(request, 'modify_project.html', context)
    messages.error(request, INACTIVE_PROJECT)
    return redirect("/")

# delete project by id
def delete_project(request, project_id):
    project=projects.get_projectbyid(id=project_id)
    if project.is_active():
        if project.delete(id=project_id):
            messages.success(request, DELETE_SUCCESSFUL)
        else:
            messages.error(request, DELETE_FAIL)
    else:
        messages.error(request, INACTIVE_PROJECT)
    return redirect("/")

# update project status to testing
def initiate_projecttesting(project_id):
    project = projects.get_projectbyid(id=project_id)
    if project.project_status ==1:
        project.project_status =2
        project.date_initiated=datetime.datetime.today()
        project.save()
    return project

# update project status to completed
def complete_projecttesting(project_id):
    project = projects.get_projectbyid(id=project_id)
    if project.is_complete():
        project.project_status = 3
        project.save()
    return project

# Cancel project : Cancel can only be completed if 
# project is under testing otherwise it can be deleted before testing 
# begins
def cancel_project(request, project_id):
    project = projects.get_projectbyid(id=project_id)
    try:
        if project.project_status != 1:
            project.project_status = 4 
            project.save()
            for sample in project.project_samples.all():
                cancel_sampleid(sample.id)
            messages.success(request, CANCEL_SUCCESS)
        return redirect('all_activeprojects')
    except:
        messages.error(request, CANCEL_ERROR)
        allprojects = projects.objects.filter(active=True)
        samplecount = projects.objects.annotate(count=Count('project_samples'))
        context={'project':allprojects, 'samplecount':samplecount}
        return render(request, 'all_activeprojects.html', context)


# Update status of sample tests, sample and project to testing
def initiate_testing(request, project_id, sampletesting_id):
    try:
        track_test = initiate_trackingtesting(sampletesting_id)
        sample = initiate_sample(track_test.sample.id)
        project = initiate_projecttesting(project_id)
        if project.project_status == 2 & sample.sample_status == 2 & track_test.test_status == 2:
            sample = samples.get_byproject(project)
            sample_tests = Sample_Testing.objects.all()
            messages.success(request, INITIATE_TESTING_SUCCESS)
        return redirect('view_project', project_id=project.id)  
    except:
        messages.error(request, INITIATE_TESTING_ERROR)
        sample = samples.get_byproject(project)
        sample_tests = Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html', context)

# Update status of sample tests, sample and project to completed. 
def complete_testing(request, project_id, sampletesting_id):
    try:
        track_test=complete_tracktesting(sampletrack_id=sampletesting_id)
        sample =complete_sample(sample_id=track_test.sample.id)
        project =complete_projecttesting(project_id=project_id)
        return redirect('view_project', project_id=project.id)
    except:
        messages.error(request,UPDATE_ERROR)
        sample = samples.get_byproject(project)
        sample_tests=Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html', context)