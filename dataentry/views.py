from django.shortcuts import render , redirect
from . utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command  # trigger commands from Django management commands
from django.contrib import messages  # for displaying messages in templates
from .tasks import import_data_task  # Celery task for importing data
from dataentry.utils import check_csv_errors  # function to check for CSV errors

# Create your views here.

def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')    # FILES is used to handle file uploads in Django
        model_name = request.POST.get('model_name')

        # store thids file inside the Upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name) 

        # construct the full path
        relative_path = str(upload.file.url)   # upload - upload/<file_name>.csv  
#        print(relative_path)  #  /media/uploads/<file_name>.csv
        base_url = str(settings.BASE_DIR)  # base url 
#        print(base_url)

        file_path = base_url + relative_path
#        print(file_path)

        # check for the csv errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))  # if there are any errors in the CSV file, show the error message to the user
            return redirect('import_data')  # redirect to the same page if there are errors


        # handle the import data task here
        import_data_task.delay(file_path, model_name)  # call the Celery task to import data asynchronously passing the file path and model name

    
        # trigger the import data command  ( )
#        try:
#            call_command('importdatafromcsv', file_path, model_name)
#            messages.success(request, 'Data imported successfully!')  # success message
#        except Exception as e:
#            messages.error(request, str(e))  # error message if something goes wrong    


        # show the message to the user
        messages.success(request, 'Your data is being imported, You will be notified once it is done.')  # success message


        return redirect('import_data')  # redirect to the same page after uploading the file


    else: 
        custom_models = get_all_custom_models()       #  function call to get all custom models from utils.py
#        print(custom_models)
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/importdata.html', context)