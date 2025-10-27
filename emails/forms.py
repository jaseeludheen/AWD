from django import forms
from .models import Email
from ckeditor.widgets import CKEditorWidget


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'
        widgets = {
            'body': CKEditorWidget(),
        }
