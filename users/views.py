from django.shortcuts import render
from django.template import context
from .models import LIMSuser, LIMSuserForm
# Create your views here.
def add_user(request):
    if request.method == 'POST':
        form = LIMSuserForm(request.POST)
        if form.is_valid():
            form.save()
    form = LIMSuserForm()
    context = {'user_form': form}
    return render(request, 'add_user.html',context)