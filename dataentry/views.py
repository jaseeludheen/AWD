from django.shortcuts import render , redirect
from . utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command  # trigger commands from Django management commands

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
        print(file_path)


        # trigger the import data command 
        try:
            call_command('importdatafromcsv', file_path, model_name)
        except Exception as e:
            raise e



        return redirect('import_data')  # redirect to the same page after uploading the file


    else: 
        custom_models = get_all_custom_models()       #  function call to get all custom models from utils.py
#        print(custom_models)
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/importdata.html', context)