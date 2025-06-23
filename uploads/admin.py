from django.contrib import admin
from .models import Upload

# Register your models here.

class UploadAdmin(admin.ModelAdmin):    # to customize the admin interface for the Upload model
    list_display = ('model_name', 'uploaded_at')   # to shows the model_name and uploaded_at fields in the list view


admin.site.register(Upload, UploadAdmin)

