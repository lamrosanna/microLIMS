from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pprint import pprint

from .models import projectForm, projects
from samples.models import samples

# Change to unfinished projects
@login_required
def home(request):
    project = projects.objects.all()
    context={"project":project}
    return render(request, 'index.html', context)

def add_project(request):
    if request.method == 'POST':
        form = projectForm(request.POST)
        if form.is_valid():
            form.save()

    form= projectForm()
    project = projects.objects.all()
    context= {'form': form, 'project':project}
    return render(request, 'add_projects.html', context)

def view_project(request, project_id):
    #need validation to check user credentials
    project=projects.get_projectbyid(project_id)
    context={"project":project}
    return render(request, 'view_project.html',context)

def view_allproject(request):
    project = projects.objects.all()
    context={"project":project}
    return render(request, 'all_projects.html', context)