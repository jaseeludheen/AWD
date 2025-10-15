from awd_main.celery import app 
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings   #  from email
import ssl
from django.core.mail import send_mail
from .utils import  generate_csv_file
from .utils import send_email_notification


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
    mail_subject = 'Import Data Completed'
    message = 'Your data import has been successful'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, [to_email])
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


@app.task
def send_email():
    mail_subject = 'Test Email from Automate with Django'
    message = 'This is a test email sent from Automate with Django project'
    to_email = settings.DEFAULT_TO_EMAIL  
    send_email_notification(mail_subject, message, to_email)
    return 'Email sent successfully'




@app.task
def export_data_task(model_name):
    try :
        # trigger call command
        call_command('exportdata', model_name)
    except Exception as e:
            raise e
    
    file_path = generate_csv_file(model_name)
#    print('file_path==>', file_path)
        
    # send email with attachment
    mail_subject = 'Export Data Successful'
    message = 'Export Data Successful. Please find the Attachment'
    to_email = settings.DEFAULT_TO_EMAIL
    
    

    send_email_notification(mail_subject, message, [to_email], attachment=file_path)
    return 'Export Data task executed successfully.'
