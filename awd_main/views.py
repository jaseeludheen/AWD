from django.shortcuts import render
from django.http import HttpResponse
import time

def home(request):
    return render(request, 'home/home.html')


def celery_test(request):
    # execute a time consuming task here
    time.sleep(10) # simulation of any task that's going to take 10 seconds
    
    return HttpResponse('<h3>Celery is working!</h3>')