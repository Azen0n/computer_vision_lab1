import base64
import io
import random
import urllib
from matplotlib import pyplot as plt


def get_plot(max_value):
    if type(max_value) != int:
        max_value = int(max_value)
    x = [i + 1 for i in range(max_value)]
    y = []
    y_value = 0
    for i in range(max_value):
        y_value += random.randint(-10, 10)
        y.append(y_value)

    fig = plt.figure()
    plt.plot(x, y)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return 'data:image/png;base64,' + urllib.parse.quote(string)


max_value = 100
uri = get_plot(max_value)


def get_image_size(image):
    print(1)
