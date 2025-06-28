from awd_main.celery import app 
import time


@app.task     # This decorator registers the function as a Celery task # Celery task
def celery_test_task():
    time.sleep(10) # simulation of any task that's going to take 10 seconds
    return 'Sample task executed successfully!'
