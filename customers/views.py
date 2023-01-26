from django.shortcuts import render
from django.template import context
from pprint import pprint
import requests
from .models import company, companyForm



# Create your views here.
def home(request):
    return render(request, 'index.html',{})

def add_company(request):
        if request.method == 'POST':
            form = companyForm(request.POST)
            if form.is_valid():
                print("success")
                form.save()
                
        else:
            print("testing")
        form=companyForm()
        x = company.objects.all()
        return render(request, 'add_company.html',{
            'form':form,
            'companies':x
    })

def viewcompany(request):
    companydetails = company.objects.all()
    context={ 'companydetails':companydetails }
    return render(request, 'view_company.html',context)

def viewcompany_company(request, company_id):
    comp = company.objects.all()
    context={'viewall':comp}
    return render(request, 'customers/view_company.html',context)   
