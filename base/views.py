import base64
import urllib
from django.shortcuts import render
from . import plots
from django import forms


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
    plot = plots.get_name_plot()
    # plot_form = PlotForm(request.POST or None)
    # if plot_form.is_valid():
    #     max_value = plot_form.cleaned_data.get('max_value')
    #     image = plots.get_plot(max_value)

    image = None
    if request.method == 'POST':
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            file = request.FILES['image'].file
            string = base64.b64encode(file.read())
            image = 'data:image/png;base64,' + urllib.parse.quote(string)
    else:
        image_form = UploadImageForm()

    context = {'image': image,
               'plot': plot,
               'image_form': image_form}
    return render(request, 'index.html', context)
