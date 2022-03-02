import base64
import urllib

from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
from . import plots
from django import forms

from base.lab2.lab2_processing import methods as methods2, get_image_as_string, mean_squared_error, mean_absolute_error, delta
from base.lab3 import methods as methods3

methods = dict(methods2).update(methods3)


class PlotForm(forms.Form):
    max_value = forms.CharField(max_length=3)
    max_value.widget.attrs.update({'id': 'maxValue',
                                   'class': 'form-control'})


class UploadImageForm(forms.Form):
    image = forms.FileField(allow_empty_file=False,
                            widget=forms.FileInput(attrs={'accept': 'image/png, image/bmp, image/tiff'}))
    image.widget.attrs.update({'id': 'image-form',
                               'class': 'form-control'})


def lab1(request):
    image = None
    width = None
    height = None
    rgb_plots = [None, None, None]
    luminosity_plot = None

    if request.method == 'POST':
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            file = request.FILES['image'].file
            image = 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(file.read()))
            image_size = Image.open(file).size
            width = image_size[0]
            height = image_size[1]
            rgb_plots = plots.get_rgb_plots(file)
            luminosity_plot = plots.get_luminosity_plot(file)
    else:
        image_form = UploadImageForm()

    context = {'image': image,
               'width': width,
               'height': height,
               'red_plot': rgb_plots[0],
               'green_plot': rgb_plots[1],
               'blue_plot': rgb_plots[2],
               'luminosity_plot': luminosity_plot,
               'image_form': image_form}
    return render(request, 'lab1.html', context)


def lab2(request):
    image = None
    image_size = None

    if request.method == 'POST':
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            file = request.FILES['image'].file
            image = 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(file.read()))
            image_size = Image.open(file).size
            image_size = f'{image_size[0]}x{image_size[1]}'
    else:
        image_form = UploadImageForm()

    context = {'image': image,
               'image_size': image_size,
               'image_form': image_form}
    return render(request, 'lab2.html', context)


def lab3(request):
    image = None
    image_size = None

    if request.method == 'POST':
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            file = request.FILES['image'].file
            image = 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(file.read()))
            image_size = Image.open(file).size
            image_size = f'{image_size[0]}x{image_size[1]}'
    else:
        image_form = UploadImageForm()

    context = {'image': image,
               'image_size': image_size,
               'image_form': image_form}
    return render(request, 'lab3.html', context)


def processing(request):
    image_file = request.FILES.get('image')
    method = request.POST.get('method')
    params = request.POST.get('param')
    image = Image.open(image_file)

    if params is None:
        processed_image = get_image_as_string(methods[method](image))
    else:
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
        processed_image = get_image_as_string(methods[method](image, *new_params))

    context = {'image': processed_image}
    return JsonResponse(context)


def metric(request):
    metric_ = request.POST.get('metric')
    image_file = request.FILES.get('image')
    image = Image.open(image_file)

    processed_image_file = request.FILES.get('processedImage')
    processed_image = Image.open(processed_image_file)

    ans = None
    if metric_ == 'mean_squared_error':
        ans = mean_squared_error(image, processed_image)
    elif metric_ == 'mean_absolute_error':
        ans = mean_absolute_error(image, processed_image)
    elif metric_ == 'delta':
        ans = delta(image, processed_image)

    context = {'ans': ans}
    return JsonResponse(context)
