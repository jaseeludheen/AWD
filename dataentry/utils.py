from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings 



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
    


def send_email_notification(mail_subject, message,to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e
