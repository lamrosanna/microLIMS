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
    path('<int:project_id>/cancel/', projects.cancel_project, name='cancel_project'),
    path('<int:project_id>/canceltest/<int:testing_id>/', test.cancel_test, name='cancel_test'),
    path('<int:project_id>/deletetest/<int:testing_id>/', test.delete_sampleTest, name='delete_test'),
    path('<int:project_id>/add_sample/', samples.add_sample, name="add_sample"),
    path('<int:project_id>/samples/<int:sample_id>/modify/', samples.modify_sample, name="modify_sample"),
    path('<int:project_id>/samples/<int:sample_id>/delete/', samples.delete_sample, name="delete_sample"),
    path('<int:project_id>/initiate_testing/<int:sampletesting_id>/', projects.initiate_testing, name="initiate_testing"),
    path('<int:project_id>/complete_testing/<int:sampletesting_id>/', projects.complete_testing, name="complete_testing"),
    
]
companypatterns=[
    path('<int:company_id>/', customers.viewcompany_company, name ='viewcompany_company'),
    path('<int:company_id>/modify/', customers.modify_company, name ='modify_company'),
    path('<int:company_id>/delete/', customers.inactivate_company, name ='inactivate_company'),
    path('<int:company_id>/add_user/',users.addcompany_user, name="addcompany_user"),
    path('<int:company_id>/user/<int:user_id>/modify/',users.modify_user, name="modify_user"),
    path('<int:company_id>/projects/', projects.view_allproject, name='view_allproject'),
]
testpatterns=[
    path('',test.add_test, name='add_test'),
    path('deactivate/<int:test_id>', test.deactivate_test, name="deactivate_test")
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
    path('tests/', include(testpatterns)),
    path('add_project/', projects.add_project, name="add_project"),
    path('add_user/', users.add_user, name="add_user"),

]
