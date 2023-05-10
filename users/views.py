from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LIMSuserForm

UNSUCCESSFUL_SIGNIN="Your log-in attempt was unsuccessul. Please try again."

def add_user(request):
    if request.method == 'POST':
        form = LIMSuserForm(request.POST)
        if form.is_valid():
            form.save()
    form = LIMSuserForm()
    context = {'form': form}
    return render(request, 'add_user.html',context)

def authenticate_view(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        # successful login
    else:
        
        return{"message":UNSUCCESSFUL_SIGNIN}

def logout_view(request):
    logout(request)
