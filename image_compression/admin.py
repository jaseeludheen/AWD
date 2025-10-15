from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html


class CompressImageAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.compressed_image.url}" width="40" height="40" />')

    def orginal_image_size(self, obj):
        return format_html(f'<span>{obj.original_image.size / (1024*1024):.2f} MB</span>')  
    
    def compressed_image_size(self, obj):
        size_in_mb = obj.compressed_image.size / (1024*1024)

        if size_in_mb > 1:   
            return format_html(f'<span>{size_in_mb:.2f} MB</span>')
        else:
            size_in_kb = obj.compressed_image.size / 1024
            return format_html(f'<span>{size_in_kb:.2f} KB</span>')


    list_display = ('user', 'thumbnail', 'orginal_image_size', 'compressed_image_size', 'compressed_at')



admin.site.register(CompressImage, CompressImageAdmin)



