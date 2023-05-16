from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from .models import test, testdetailsForm
from customers.models import company

def add_test(request, company_id):
    test_company = company.get_byid(id=company_id)
    check = reverse(add_test, args=[company_id])
    if request.method == 'POST': 
        form=testdetailsForm(request.POST)
        if form.is_valid():
            form.instance.company=test_company
            form.save()
    form=testdetailsForm()
    test_detail=test.get_bycompany(company_id)
    context = {'test':form,'listed_tests': test_detail, 'company':test_company}
    return render(request, 'add_tests.html',context)

def view_test(request):
    tests = test.get_all()
    context={'tests':tests}
    return render(request, 'view_tests.html', context)