import base64
import urllib

from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
from . import plots
from django import forms

from .lab2_processing import methods, get_image_as_string


class PlotForm(forms.Form):
    max_value = forms.CharField(max_length=3)
    max_value.widget.attrs.update({'id': 'maxValue',
                                   'class': 'form-control'})


class UploadImageForm(forms.Form):
    image = forms.FileField(allow_empty_file=False,
                            widget=forms.FileInput(attrs={'accept': 'image/png, image/bmp, image/tiff'}))
    image.widget.attrs.update({'id': 'image-form',
                               'class': 'form-control'})


def index(request):
    image = None
    image_size = None
    rgb_plots = [None, None, None]
    luminosity_plot = None

    if request.method == 'POST':
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            file = request.FILES['image'].file
            image = 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(file.read()))
            image_size = Image.open(file).size
            image_size = f'{image_size[0]}x{image_size[1]}'
            rgb_plots = plots.get_rgb_plots(file)
            luminosity_plot = plots.get_luminosity_plot(file)
    else:
        image_form = UploadImageForm()

    context = {'image': image,
               'image_size': image_size,
               'red_plot': rgb_plots[0],
               'green_plot': rgb_plots[1],
               'blue_plot': rgb_plots[2],
               'luminosity_plot': luminosity_plot,
               'image_form': image_form}
    return render(request, 'index.html', context)


def processing(request):
    image_file = request.FILES.get('image')
    method = request.POST.get('method')
    params = request.POST.get('param')
    image = Image.open(image_file)

    params = params.split(',')
    new_params = []
    for param in params:
        try:
            new_params.append(int(param))
        except:
            try:
                new_params.append(float(param))
            except:
                new_params.append(param)

    if new_params is None:
        processed_image = methods[method](image)
    else:
        processed_image = get_image_as_string(methods[method](image, *new_params))

    context = {'image': processed_image}
    return JsonResponse(context)
