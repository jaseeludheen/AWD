from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CompressImageForm
from PIL import Image
import io





def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_image']
            quality = form.cleaned_data['quality']

            compressed_img = form.save(commit=False) # commit=False means do not save to database yet , temperary save because still  want to manipulate
            compressed_img.user = user  # assign the user to the model instance

            # perform compression
            img = Image.open(original_img)

            output_format = img.format

            buffer = io.BytesIO() # buffer to store images's binary data , but it actually create a virtual memory  for storing image data
            print('curser position at the beginning=>', buffer.tell()) # tell() method tells the current position of the cursor in the buffer


            img.save(buffer, format=output_format, quality=quality)
            print('curser position after image compression=>', buffer.tell()) 
            
            buffer.seek(0) # move the cursor to the beginning of the buffer
            print('curser position after setting back to 0=>', buffer.tell()) 

            # save the compressed image to the model
            compressed_img.compressed_image.save(
                f'compressed_{original_img}', buffer
            )

            #Atomatically download the compressed image
            response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
            return response  # response
#            return redirect('compress')


    else:       
        form = CompressImageForm()
        context = {
            'compress_form': form
        }
    return render(request, 'image_compression/compress.html', context)