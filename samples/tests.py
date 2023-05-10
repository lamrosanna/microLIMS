from django.test import TestCase
import datetime
from customers.models import company # needed to generate project
from projects.models import projects # needed to generate samples
from samples.models import samples #samples
from test_methods.models import test

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
            test_TAT ="1"
        )
        test1.save()
        test2=test.objects.create(
            test_name="Test Method 2", 
            test_code="2", 
            testMethod="USP", 
            test_type="1",
            test_TAT ="2"
        )
        test2.save()
        test3=test.objects.create(
            test_name="Test Method 3", 
            test_code="3", 
            testMethod="USP", 
            test_type="1",
            test_TAT ="3"
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
    def test_startTesting(self):

        project1 = projects.objects.get(project_name="Test Project Name")
        # self.assertEqual(project1.project_po, "92308")

        # sample2 = samples.get_byid(1)
        # sample3 = sample2.get_allanalysis()
        # #testing = sample2.is_testingfinished()
        # self.assertEqual(sample3, False)
        project2 = project1.project_samples.all()
        self.assertEqual(project2, None)
