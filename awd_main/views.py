from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import time
from dataentry.tasks import celery_test_task, send_test_email_task
from .forms import LoginForm, RegistrationForm 
from django.contrib import messages, auth
from django.shortcuts import redirect



@login_required(login_url='login')
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
            return render(request, 'user/register.html' , context)

  
    else:
        form = RegistrationForm()
        context ={
            'form': form,
        }
    return render(request, 'user/register.html', context)



def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'user/login.html', {'form': form})
        else:
            messages.error(request, 'Invalid form submission')
            return render(request, 'user/login.html', {'form': form})
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')