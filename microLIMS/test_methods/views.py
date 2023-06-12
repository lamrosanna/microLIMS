from django.shortcuts import render, redirect
from django.contrib import messages


from .models import test, testdetailsForm, Sample_Testing
from customers.models import company
from projects.models import projects
from samples.models import samples

#errors
CANCEL_ERROR="There was an error in cancelling test."
CANCEL_SUCCESS="Your test was cancelled."
TEST_EXISTS="A Test with that name/code already exists."
TEST_CREATION_SUCCESS="Test created successfully."
DEACTIVATE_ERROR="There was an error deactivating test"
DEATIVATE_SUCCESS="Test was successfully deactivated"
ACTIVATE_SUCCESS="Test was successfully activated."
ACTIVATE_ERROR="There was an error in activating test."
DELETE_SUCCESS="Test was deleted."
DELETE_ERROR="There was an error in deleting test."

# Create Test
def add_test(request):
    if request.method == 'POST': 
        form=testdetailsForm(request.POST)
        if form.is_valid():
            testname = request.POST.get('test_name')
            testcode = request.POST.get('test_code')
            if test.objects.filter(test_name=testname).exists() or test.objects.filter(test_code=testcode).exists():
                messages.error(request, TEST_EXISTS)
            else:
                form.save()
                messages.success(request, TEST_CREATION_SUCCESS)
    form = testdetailsForm()
    test_detail = test.objects.order_by("test_name")
    context = {'form':form,'tests': test_detail}
    return render(request, 'view_tests.html',context)


# cancel test by id
def cancel_test(request, project_id, testing_id ):
    sample_test=Sample_Testing.get_byid(id=testing_id)
    project = projects.get_projectbyid(id=project_id)
    if sample_test:
        try:
            sample_test.test_status=4
            sample_test.save()
            messages.success(request, CANCEL_SUCCESS)
            return redirect('view_project', project_id=project.id)
        except:
            messages.error(request, CANCEL_ERROR)
            sample = samples.get_byproject(project)
            sample_tests=Sample_Testing.objects.all()
            context = {"project":project, 'samples':sample, 'tests':sample_tests}
            return render(request, 'view_project.html', context)

# deactivate test method
def deactivate_test(request, test_id):
    activeTests = test.get_byid(id=test_id)
    if activeTests.active==True:
        activeTests.active=False
        activeTests.save()
        messages.success(request, DEATIVATE_SUCCESS)
        return redirect('add_test')
    messages.error(request, DEACTIVATE_ERROR)
    form = testdetailsForm()
    test_detail = test.objects.order_by("test_name")
    context = {'form':form,'tests': test_detail}
    return render(request, 'view_tests.html', context)

def activate_test(request, test_id):
    activeTests = test.get_byid(id=test_id)
    if activeTests.active == False:
        activeTests.active=True
        activeTests.save()
        messages.success(request, ACTIVATE_SUCCESS)
        return redirect('add_test')
    messages.error(request, ACTIVATE_ERROR)
    form = testdetailsForm()
    test_detail = test.objects.order_by("test_name")
    context = {'form':form,'tests': test_detail}
    return render(request, 'view_tests.html', context)

# delete test from sample before testing
def delete_sampleTest(request, project_id, testing_id):
    sample_test=Sample_Testing.get_byid(id=testing_id)
    project = projects.get_projectbyid(id=project_id)
    sample=samples.get_byid(id=sample_test.sample.id)
    try:
        Sample_Testing.delete(sample_test.id)
        messages.success(request, DELETE_SUCCESS)
        return redirect('view_project', project_id=project.id)
    except:
        messages.error(request, DELETE_ERROR)
        sample = samples.get_byproject(project)
        sample_tests=Sample_Testing.objects.all()
        context = {"project":project, 'samples':sample, 'tests':sample_tests}
        return render(request, 'view_project.html', context)
        
# cancel all sample testing by sample id
def cancel_alltesting(sample_id):
    sample = samples.get_byid(id=sample_id)
    sampletests=Sample_Testing.get_bysample(sample)
    for test in sampletests:
        test.test_status=4
        test.save()

# create sampletesting object for sample and each attributed test
def create_sampletesting(sample_id):
    sample = samples.get_byid(id=sample_id)
    for analysis in sample.analysis.all():
        tests= test.get_byname(analysis)
        test_samples=Sample_Testing(testing=tests, sample=sample)
        test_samples.save()

# update sample test tracking status to testing(2)
def initiate_trackingtesting(id):
    trackingtest = Sample_Testing.get_byid(id=id)
    if trackingtest.test_status == 1:
        trackingtest.test_status = 2
        trackingtest.save()
    return trackingtest
    
# update sample test tracking status to complete(3)
def complete_tracktesting(id):
    trackingtest = Sample_Testing.get_byid(id=id)
    if trackingtest.test_status == 2:
        trackingtest.test_status = 3
        trackingtest.save()
    return trackingtest