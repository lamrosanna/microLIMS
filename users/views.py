from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import LIMSuserForm, companyuserForm, LIMSuserChangeForm
from .models import LIMSuser
from customers.models import company

INVALID_LOGIN="Email/password was not recognized."
AUTHENTICATION_FAILED="Email/password was not authenticated"


def add_user(request, company_id):
    user_company = company.get_byid(id=company_id)
    if request.method == 'POST':
        form = LIMSuserForm(request.POST)
        if form.is_valid():
            form.instance.company=user_company
            form.save()
    form = LIMSuserForm()
    context = {'form': form, 'company':user_company}
    return render(request, 'add_user.html',context)

def add_user_noCompany(request):
    if request.method == 'POST':
        form = companyuserForm(request.POST)
        if form.is_valid():
            form.save()
    form = LIMSuserForm()
    context = {'form': form}
    return render(request, 'add_user.html',context)

def modify_user(request, user_id, company_id):
    user = LIMSuser.get_byid(id=user_id)
    user_company = company.get_byid(id=company_id)
    form = LIMSuserChangeForm(instance=user)
    if request.method == 'POST':
        form=LIMSuserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user_company_id=form.cleaned_data['company']
            user_company=company.get_byid(user_company_id)
            form.save()
            return redirect('view_project')
    users=LIMSuser.get_bycompany(user_company)
    context = {'form':form, 'company':user_company,'users':users}
    return render(request, 'modify_user.html', context)

def LoginView(request):
    if request.method == 'POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                Limsuser = LIMSuser.objects.get(email=username)
                return redirect('/', user=Limsuser)
            else:
                messages.error(request, INVALID_LOGIN)
        else:
            print('2')
            messages.error(request, AUTHENTICATION_FAILED)   
    form=AuthenticationForm()
    #context={"login_form":form }
    return render(request, 'registration/login.html', context={"login_form":form })

def LogoutView(request):
    logout(request)
    return render(request, 'registration/logout.html')
