"""apitests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apitest1 import views as co
from test_methods import views as testd

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', co.home, name='index'),
    path('add_company/', co.add_company, name='add_company'),
    path('viewcompany/',co.viewcompany, name ='viewcompany'),
    path('viewcompany/<int:company_id>/',co.viewcompany_company, name ='viewcompany_company'),
    path('add_test/', testd.add_test, name='add_test'),
    
]
