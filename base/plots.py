import base64
import io
import random
import urllib
from matplotlib import pyplot as plt


def get_plot(max_value: int) -> str:
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

    return get_plot_as_string(fig)


def get_plot_as_string(fig: plt.Figure) -> str:
    """Превращает изображение графика в строку."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return 'data:image/png;base64,' + urllib.parse.quote(string)


def get_name_plot() -> str:
    fig = plt.figure()

    # График создавать тут
    plt.plot([100, 20, 30, 40, 50], [1, 2, 3, 4, 5])

    return get_plot_as_string(fig)
