from awd_main.celery import app 
import time
from django.core.management import call_command


@app.task     # This decorator registers the function as a Celery task # Celery task
def celery_test_task():
    time.sleep(10) # simulation of any task that's going to take 10 seconds
    return 'Sample task executed successfully!'



@app.task
def import_data_task(file_path, model_name):

    try:
        call_command('importdatafromcsv', file_path, model_name)
    except Exception as e:
        raise e
    # notify the user by email
    
    return ('Data imported successfully!')
  