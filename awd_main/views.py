from django.shortcuts import render
from django.http import HttpResponse
import time
from dataentry.tasks import celery_test_task, send_test_email_task
from .forms import RegistrationForm 
from django.contrib import messages
from django.shortcuts import redirect




def home(request):
    return render(request, 'home/home_page.html')


def celery_test(request):
    # execute a time consuming task here
    celery_test_task.delay()  # This will run the task asynchronously
    
    return HttpResponse('<h3>Celery is working!</h3>')



def email_test(request):
    
    send_test_email_task.delay()  # This will run the task asynchronously
    
    return HttpResponse('<h3>Email sent successfully!</h3>')  # This will be displayed immediately after the task is triggered


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('register')  
        else:
            context = {
                'form': form,
            }
            return render(request, 'user/register1.html' , context)

  
    else:
        form = RegistrationForm()
        context ={
            'form': form,
        }
    return render(request, 'user/register1.html', context)



def login(request):
    return render(request, 'user/login.html')


