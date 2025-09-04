from django.contrib import admin
from .models import List, Subscribers, Email



# Register your models here.

admin.site.register(List)
admin.site.register(Subscribers)
admin.site.register(Email)

