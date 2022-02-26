import base64
import urllib
from django.shortcuts import render
from . import plots
from django import forms
from PIL import Image


class PlotForm(forms.Form):
    max_value = forms.CharField(max_length=3)
    max_value.widget.attrs.update({'id': 'maxValue',
                                   'class': 'form-control'})


class UploadImageForm(forms.Form):
    image = forms.FileField(allow_empty_file=False,
                            widget=forms.FileInput(attrs={'accept': 'image/png, image/bmp, image/tiff'}))
    image.widget.attrs.update({'id': 'image-form',
                               'class': 'form-control'})

def upload(request):
    if request.method == 'POST':
        print(2)
    context = {'image': 4}
    return render(request, 'index.html', context)


def index(request):
    plot = None
    plotR = None
    plotG = None
    plotB = None
    # plot_form = PlotForm(request.POST or None)
    # if plot_form.is_valid():
    #     max_value = plot_form.cleaned_data.get('max_value')
    #     image = plots.get_plot(max_value)

    image = None
    imMain = None

    if request.method == 'POST':
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            file = request.FILES['image'].file
            string = base64.b64encode(file.read())
            image = 'data:image/png;base64,' + urllib.parse.quote(string)
            imMain = Image.open(file)
            plots.imageMain = imMain
    else:
        image_form = UploadImageForm()
    if image != None:
        plotR = plots.get_chart_plot(imMain, 0)
        plotG = plots.get_chart_plot(imMain, 1)
        plotB = plots.get_chart_plot(imMain, 2)
        plotY = plots.get_chart_plot(imMain, 3)
    context = {'image': image,
               'plot': plot,
               'plotR': plotR,
               'plotG': plotG,
               'plotB': plotB,
               'plotY': plotY,
               'image_form': image_form}
    return render(request, 'index.html', context)
