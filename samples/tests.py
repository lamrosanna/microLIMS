from django.test import TestCase
import datetime
from customers.models import company # needed to generate project
from projects.models import projects # needed to generate samples
from samples.models import samples #samples
from users.models import LIMSuser
from test_methods.models import test, Sample_Testing
from django.shortcuts import get_list_or_404

class SamplesTestCase(TestCase):
    def setUp(self):
        customer = company.objects.create(
            company_name="Test Company 1",
            customer_contact="Test Contact 1", 
            address="Test Address 123", 
            city="Test",
            state="CO", 
            phone="999999999",
            entity="CUSTOMER")
        customer.save()
        project = projects.objects.create(
            project_name="Test Project Name", 
            project_po="92308",
            company=company.objects.get(company_name="Test Company 1")
        )
        project.save()
        test1=test.objects.create(
            test_name="Test Method 1", 
            test_code="1", 
            testMethod="USP", 
            test_type="1",
            test_TAT ="1",
        )
        test1.save()
        test2=test.objects.create(
            test_name="Test Method 2", 
            test_code="2", 
            testMethod="USP", 
            test_type="1",
            test_TAT ="2",
        )
        test2.save()
        test3=test.objects.create(
            test_name="Test Method 3", 
            test_code="3", 
            testMethod="USP", 
            test_type="1",
            test_TAT ="3",
        )
        test3.save()
        analysis_list=[test1,test2,test3]
        sample = samples.objects.create(
            sample_name= "Sample Test 1",
            sample_description="Sample description 1",
            sample_project=projects.objects.get(project_name="Test Project Name"),
            sample_created=datetime.datetime.now(),
            sample_status=3
        )
        sample.analysis.set(analysis_list)
        sample.save()
        samplelist = [sample]
        project.project_samples.set(samplelist)
        testcompany = company.objects.get(company_name="Test Company 1")
        user = LIMSuser.objects.create_user(email="normal@user.com", password="foo", company_id=testcompany.id)
        user.save()

        for tests in sample.analysis.all():
            sampletest=Sample_Testing(testing=tests, sample=sample)
            sampletest.save()
    def test_startTesting(self):
        sample = samples.get_byid(1)
        sampletests = Sample_Testing.get_bysample(sample)
        for each in sampletests:
            each.test_status = 3
            each.save()
        samplecomplete= Sample_Testing.is_testingcomplete(sample)
        
        self.assertEqual(samplecomplete, True)
    def test_projectcomplete(self):
        project = projects.get_projectbyid(1)
        for eachsample in project.project_samples.all():
            eachsample.sample_status = 3
            eachsample.save()
        projectcomplete = project.is_complete()
        self.assertEqual(projectcomplete,True)