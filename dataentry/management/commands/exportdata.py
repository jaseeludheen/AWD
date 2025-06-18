from django.core.management.base import BaseCommand
from django.apps import apps
import csv
import datetime

# proposed command - python manage.py exportdata model_name


class Command(BaseCommand):
    help = 'Export student data to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model to export data from')


    def handle(self, *args, **kwargs):

        model_name = kwargs['model_name'].capitalize()  # Capitalize the model name to match Django's convention

        # search for the model in all installed apps
        model = None

        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break  # stop searching once the model is found
            except LookupError:
                pass

        if not model:
            self.stdout.write(self.style.ERROR(f'Model "{model_name}" not found in any app.'))
            return
        

        data = model.objects.all()

        # generate the timestamp of current data and time
        timestamp = datetime.datetime.now().strftime("%I:%M:%S %p %d-%m-%Y")
        
        # define the CSV file name / path
        file_path = f'exported_{model_name}_data_{timestamp}.csv'
        # open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            # write the CSV header
            #print the field names dynamically
            writer.writerow([field.name for field in model._meta.fields]) # list comprehension to get the field names dynamically

            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])  # list comprehension to get the field values dynamically

            self.stdout.write(self.style.SUCCESS('Data exported successfully!'))


        

