from django.shortcuts import render,redirect
from django.contrib import messages

from projects.models import projects
from samples.models import samples
from .models import company, companyForm
from users.models import LIMSuser

DELETE_SUCCESSFUL="Company was successfully deleted"
DELETE_FAIL="There was an error in deleting company"
ERROR_INSERTING = "An error occured while inserting the item."

# only admin should have permission to create company
def add_company(request):
        if request.method == 'POST':
            form = companyForm(request.POST)
            if form.is_valid():
                # perform check to see if another company already has the same name
                form.save()
                #return JsonResponse({"message":"New company information saved successfully"}, status=202)
            #return{"message":ERROR_INSERTING}, 400
        form=companyForm()
        x = company.objects.all()
        return render(request, 'add_company.html',{
            'form':form,
            'companies':x
    })
# only admin should have permission to view all company
def viewcompany(request):
    companydetails = company.objects.filter(active=True)
    context={ 'companies':companydetails }
    return render(request, 'view_allcompany.html',context)

def viewcompany_company(request, company_id):
    companydetails = company.get_byid(company_id)
    users=LIMSuser.get_bycompany(companydetails)
    context={'company':companydetails,'users':users}
    return render(request, 'view_company.html',context)   

def modify_company(request, company_id):
    user_company=company.get_byid(id=company_id)
    form=companyForm(instance=user_company)
    if request.method == 'POST':
        form=companyForm(request.POST, instance=user_company)
        if form.is_valid():
            form.save()
    context={'form':form, 'company':user_company}

    return render(request, 'modify_company.html', context)

def inactivate_company(request, company_id):
    user_company= company.get_byid(id=company_id)
    project = projects.get_projectbycompany(user_company)
    sample = samples.get_byproject(project)
    if user_company:
        user_company.active=False
        user_company.save()
        for eachproject in project:
            eachproject.active=False
            eachproject.save()
        for eachsample in sample:
            eachsample.active=False
            eachsample.save()
        #companydetails = company.objects.filter(active=True)
        messages.success(request, DELETE_SUCCESSFUL)
        return redirect('view_company')
    else:
        messages.error(request, DELETE_FAIL)
    form=companyForm()
    companies=company.objects.filter(active=True)
    context={'companies':companies, 'form':form}
    return render(request, 'modify_company.html', context)