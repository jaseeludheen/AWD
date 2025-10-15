from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from .utils import send_email_notification
from django.conf import settings
from .models import Subscriber, Email, Sent, EmailTracking
from .task import send_email_task
from django.db.models import Sum
from django.utils import timezone



def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            # set an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')

            # access the selected email list
            email_list = email.email_list
            print('email list ==>',email_list)

            # Extract email address from the Subscriber model in the selected email list
            subscribers = Subscriber.objects.filter(email_list=email_list)  # email_list is from subscriber model , another is above

            """
            to_email = []
            for email in subscribers:
                to_email.append(email.email_address)
            print('to_email ==>',to_email)
            """
            to_email = [email.email_address for email in subscribers] # list comprehension method

            if email.attachment:
                attachment = email.attachment.path
            else: 
                attachment = None

            email_id = email.id
            # Update the email instance with the email ID

#           send_email_notification(mail_subject, message, to_email, attachment)
            # Handover email sending task to Celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id) 


            # display success message
            messages.success(request, 'Email sent successfully!')
            return redirect('send_email')
        

    else:
        email = EmailForm()
        context = {
            'email_form': email,
        }
        return render(request, 'emails/send-email.html', context)

 
def track_click(request , unique_id):
    # Logic to store the tracking info
    print(request)
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get('url')
        # check if thr clicked_at field is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
    except:
        return HttpResponse("Email Tracking Record Not Found!")

    



def track_open(request, unique_id):
    # Logic to store the tracking info
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if thr opened_at field is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email Opened Successfully")
        else:
            return HttpResponse("Email Already Opened")
    
    except:
        return HttpResponse("Email Tracking Record Not Found!")
    
        
        





def track_dashboard(request):
#   emails = Email.objects.all()
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at') # ('sent__total_sent') sent is related name in Sent model, total_sent is field name in Sent model, totat_sent is the new field name for each email instance , order by decendind set_at
    
    context = {
        'emails': emails,
    }
    return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)

    context ={
        'email': email,
        'total_sent': sent.total_sent,
    }
    return render (request, 'emails/track_stats.html', context)