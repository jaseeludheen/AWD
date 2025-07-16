from django.shortcuts import render
from django.http import HttpResponse
import time
from dataentry.tasks import celery_test_task, send_test_email_task



def home(request):
    return render(request, 'home/home_page.html')


def celery_test(request):
    # execute a time consuming task here
    celery_test_task.delay()  # This will run the task asynchronously
    
    return HttpResponse('<h3>Celery is working!</h3>')



def email_test(request):
    
    send_test_email_task.delay()  # This will run the task asynchronously
    
    return HttpResponse('<h3>Email sent successfully!</h3>')  # This will be displayed immediately after the task is triggered

