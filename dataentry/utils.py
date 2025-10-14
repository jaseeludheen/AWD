import os
from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings 
import datetime
from emails.models import Email , Sent , Subscriber 

import time
import hashlib
from emails.models import EmailTracking
from bs4 import BeautifulSoup



def get_all_custom_models():
    default_model = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'User','Upload' ]

    # try to get all models 
    custom_models = []
    for model in apps.get_models():

        if model.__name__ not in default_model:
            custom_models.append(model.__name__)

    return custom_models

#        print(model.__name__)    # list of all models




# check for the csv errors
def check_csv_errors(file_path, model_name):
    model = None  
    for app_config in apps.get_app_configs():    
        try:
            model = apps.get_model(app_config.label, model_name) 
            break  
        except LookupError:    
            continue   


    if not model:
        raise CommandError(f'Model "{model_name}" not found in any app.')

    model_fields = [field.name for field in model._meta.fields if field.name != 'id']    # excluding the id field
    model_fields_set = set([field.strip().lower() for field in model_fields])



    try:

        with open(file_path, 'r') as file:  
            reader = csv.DictReader(file)  #  first row of the CSV file is considered as the header
            # fetch the header from the csv file
            csv_header = reader.fieldnames     # header of the csv file
            csv_fields = set([field.strip().lower() for field in csv_header])  # strip() removes spaces like " Name " ➜ "Name".      lower() makes it lowercase, so "Name" ➜ "name". and  convert it to a set to allow unordered comparison.

            # compare csv header with model's field names
            """
            if csv_fields != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields.")
            """
            # Compare sets (case-insensitive, order-insensitive)
            if not model_fields_set.issubset(csv_fields):
                raise DataError(f"CSV file headers do not match the fields of the {model_name} model.\nExpected fields: {model_fields}\nCSV headers: {csv_header}")
    
    except Exception as e:
        raise e
    
    return model # return the model if no errors found, so that it can be used in the import command
    

"""
def send_email_notification(mail_subject, message, to_email, attachment=None):  # attachment=None , set default 
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=to_email)
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e
"""

"""
def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):  # attachment=None , set default 
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        for recipient_email in to_email:
            # Create EmailTracking  record
            mail = EmailMessage(mail_subject, message, from_email, to=[recipient_email])    # replace message with new_message - new_message will sent inside email body ,, to_email change to recipient_email
            if attachment is not None:
                mail.attach_file(attachment)
            
            mail.content_subtype = "html" # to send HTML email , to show html content in email body 
            mail.send()

    except Exception as e:
        raise e

"""

def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):  # attachment=None , set default 
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        for recipient_email in to_email:
            # Create EmailTracking  record

            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,   # email field name from  EmailTracking model
                    subscriber = subscriber,
                    unique_id = unique_id,
                )

                base_url = settings.BASE_URL  # add your ngrok url here
                # Generate the tracking pixel
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
                #print('click_tracking_url ==>',click_tracking_url)

                # Search for the link in email body
                
                soup = BeautifulSoup(message, 'html.parser') #html parser is analying the html content in email body
                """
                for a in soup.find_all('a', href=True): # find all anchor tags with href attribute , 
                    print(a['href'])
                """
                # List comprehension method (above code)
                urls = [ a['href'] for a in soup.find_all('a', href=True) ]
                print('urls ==>',urls) # list of all urls in the email body

                # If there are links / urls in the email body , Inject our click tracking url to that original link
                if urls:
                    new_message = message
                    for url in urls:
                        # make the final tracking url (combination of click_tracking_url and urls)
                        tracking_url = f"{click_tracking_url}?url={url}" # https://example.com/track?url=https://mywebsite.com/page1
                        #print('tracking_url ==>',tracking_url)
                        
                        new_message = new_message.replace(f"{url}", f"{tracking_url}") # Replace the existing url with tracking url in the email body
                else:
                    new_message = message
                    print("No URLs found in the email body.")


                # create theemail content with open tracking pixel image
                open_tracking_img = f'<img src="{open_tracking_url}" alt="" width="1" height="1" />'  # 1x1 pixel image

                new_message += open_tracking_img  # append the open tracking image to the email body
                

            else:
                new_message = message


            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])    # replace message with new_message - new_message will sent inside email body ,, to_email change to recipient_email
            if attachment is not None:
                mail.attach_file(attachment)
            
            mail.content_subtype = "html" # to send HTML email , to show html content in email body 
            mail.send()


        # Store the total sent emails inside the sent model
        #email = Email.objects.get(pk=email_id)

        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e
    



def generate_csv_file(model_name):
    # generate the timestamp of current data and time
    timestamp = datetime.datetime.now().strftime("%I:%M:%S%p_%d-%m-%Y")

    export_dir = 'exported_data'
    # define the CSV file name / path
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name) # 
    print('file_path==>', file_path)

    return file_path