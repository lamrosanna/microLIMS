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
from django.urls import path, re_path, reverse, include
from django.contrib.auth import views as auth_views

from customers import views as customers
from test_methods import views as testd
from users import views as users
from projects import views as projects
from samples import views as samples

projectpatterns=[
    path("", projects.view_allproject, name="view_allproject"),
    path('add_project/', projects.add_project, name="add_project"),
    re_path(r'^(?P<project_id>[0-9])/$',projects.view_project, name="view_project"),
    re_path(r'^(?P<project_id>[0-9])/add_sample/', samples.add_sample, name="add_sample"),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',users.LoginView, name='login'),
    path('logout/', users.LogoutView, name='logout'),
    path('', projects.home, name='index'),
    path('add_company/', customers.add_company, name='add_company'),
    path('viewcompany/',customers.viewcompany, name ='viewcompany'),
    path('viewcompany/<int:company_id>/',customers.viewcompany_company, name ='viewcompany_company'),
    path('add_test/', testd.add_test, name='add_test'),
    path('add_user/', users.add_user, name="add_user"),
    path('projects/', include(projectpatterns)),
]
