from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from .models import projectForm, projects
from samples.models import samples
from customers.models import company
from test_methods.models import Sample_Testing

DELETE_SUCCESSFUL="Project was successfully deleted"
DELETE_FAIL="There was an error in deleting project"

# Change to unfinished projects
@login_required
def home(request):
    project = projects.objects.filter(active=True)
    context={"project":project}
    return render(request, 'index.html', context)

def add_project(request, company_id):
    project_company = company.get_byid(id=company_id)
    if request.method == 'POST':
        form = projectForm(request.POST)
        if form.is_valid():
            form.instance.company=project_company
            form.save()

    form = projectForm()
    project = projects.objects.all()
    context= {'form':form, 'project':project, 'company':project_company}
    return render(request, 'add_projects.html', context)

def view_project(request, project_id):
    #need validation to check user credentials
    project = projects.get_projectbyid(project_id)
    sample = samples.get_byproject(project_id)
    sample_tests=[Sample_Testing.get_bysample(x) for x in sample]
    context = {"project":project, 'samples':sample, 'tests':sample_tests}
    return render(request, 'view_project.html',context)

def view_allproject(request, company_id):
    companyProject = company.get_byid(id=company_id)
    project = projects.objects.filter(company=company_id).filter(active=True)
    context = {'project':project, 'company':companyProject}
    return render(request, 'all_projects.html', context)

def all_activeprojects(request):
    allprojects = projects.objects.filter(active=True)
    context={'project':allprojects}
    return render(request, 'all_activeprojects.html', context)

def modify_project(request, project_id):
    project=projects.get_projectbyid(id=project_id)
    form = projectForm(instance=project)
    if request.method == 'POST':
        form = projectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
    context={'form':form, 'project':project}
    return render(request, 'modify_project.html', context)

def delete_project(request, project_id):
    
    if projects.delete(id=project_id):
        messages.success(request, DELETE_SUCCESSFUL)
    else:
        messages.error(request, DELETE_FAIL)
    pass

