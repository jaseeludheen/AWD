from awd_main.celery import app 
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings   #  from email
import ssl
from django.core.mail import send_mail


@app.task     # This decorator registers the function as a Celery task # Celery task
def celery_test_task():
    time.sleep(5) # simulation of any task that's going to take 10 seconds

    return 'Sample task executed successfully!'



@app.task
def import_data_task(file_path, model_name):

    try:
        call_command('importdatafromcsv', file_path, model_name)
    except Exception as e:
        raise e
    # notify the user by email

    return ('Data imported successfully!')


@app.task
def send_test_email_task(): 
    time.sleep(2)  # simulate a delay of 10 seconds before sending the email
    mail_subject = 'Test Email from Automate with Django'
    message = 'This is a test email sent from Automate with Django project'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.DEFAULT_TO_EMAIL  

#    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
#    mail.send()

    ssl._create_default_https_context = ssl._create_unverified_context


    send_mail ( 
        subject=mail_subject,
        message=message,
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
        connection=None,
        
    )

    

    return 'Test email sent successfully!'  # return a success message after sending the email