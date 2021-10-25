from django.shortcuts import render
from django.template import context
from pprint import pprint
import requests
from .models import test, testdetailsForm
# Create your views here.
def home(request):
        return render(request, 'test_methods/view_tests.html',{
    })
def add_test(request):
    if request.method == 'POST': 
        form=testdetailsForm(request.POST)
        if form.is_valid():
            form.save()
    form=testdetailsForm()
    test_detail=test.objects.all()
    context = {'test':form,'listed_tests': test_detail}
    return render(request, 'test_methods/addTest.html',context)