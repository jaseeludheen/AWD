from django.shortcuts import render

# Create your views here.

def import_data(request):

    return render(request, 'dataentry/importdata.html')