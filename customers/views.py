from django.shortcuts import render
from django.template import context
from pprint import pprint
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import requests

from .models import company, companyForm


ERROR_INSERTING = "An error occured while inserting the item."

# Create your views here.
def home(request):
    return render(request, 'index.html',{})

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

def viewcompany(request):
    companydetails = company.objects.all()
    context={ 'companydetails':companydetails }
    return render(request, 'view_company.html',context)

def viewcompany_company(request, company_id):
    companydetails = company.get_byid(company_id)
    context={'companydetails':companydetails}
    return render(request, 'view_company.html',context)   
