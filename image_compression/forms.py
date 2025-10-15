from django import forms
from .models import CompressImage



class CompressImageForm(forms.ModelForm):

    original_image = forms.ImageField(
        required=True,
        label='Upload Image',
        help_text='Upload an image to compress.',
        
    )
    

    class Meta:
        model = CompressImage
        fields = ['original_image', 'quality']
        