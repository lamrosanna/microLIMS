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
from test_methods import views as test
from users import views as users
from projects import views as projects
from samples import views as samples

projectpatterns=[
    path('', projects.all_activeprojects, name="all_activeprojects"),
    path('<int:project_id>/',projects.view_project, name="view_project"),
    path('<int:project_id>/modify/', projects.modify_project, name='modify_project'),
    path('<int:project_id>/delete/', projects.delete_project, name='delete_project'),
    path('<int:project_id>/add_sample/', samples.add_sample, name="add_sample"),
    path('<int:project_id>/samples/<int:sample_id>/modify/', samples.modify_sample, name="modify_sample"),
    path('<int:project_id>/samples/<int:sample_id>/delete/', samples.delete_sample, name="delete_sample"),
]
companypatterns=[
    path('<int:company_id>/', customers.viewcompany_company, name ='viewcompany_company'),
    path('<int:company_id>/modify/', customers.modify_company, name ='modify_company'),
    path('<int:company_id>/delete/', customers.inactivate_company, name ='inactivate_company'),
    path('<int:company_id>/add_user/',users.add_user, name="add_user"),
    path('<int:company_id>/user/<int:user_id>/modify/',users.modify_user, name="modify_user"),
    path('<int:company_id>/add_project/', projects.add_project, name="add_project"),
    path('<int:company_id>/projects/', projects.view_allproject, name='view_allproject'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',users.LoginView, name='login'),
    path('logout/', users.LogoutView, name='logout'),
    path('', projects.home, name='index'),
    path('add_company/', customers.add_company, name='add_company'),
    path('viewcompany/',customers.viewcompany, name ='viewcompany'),
    path('company/', include(companypatterns)),
    path('projects/', include(projectpatterns)),
    path('tests/', test.view_test, name='view_test'),
]
