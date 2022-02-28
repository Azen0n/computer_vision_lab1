import base64
import io
import random
import urllib
from PIL import Image
from matplotlib import pyplot as plt, font_manager
from lab1.settings import BASE_DIR
plt.rcParams.update({'font.size': 4})
font_manager.fontManager.addfont(path=f'{BASE_DIR}/OpenSans-Regular.ttf')
prop = font_manager.FontProperties(fname=f'{BASE_DIR}/OpenSans-Regular.ttf')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()
plt.rcParams['axes.linewidth'] = 0
plt.rcParams['axes.edgecolor'] = '#F4F4F4'


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
    fig.savefig(buf, bbox_inches='tight', pad_inches=0.05, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return 'data:image/png;base64,' + urllib.parse.quote(string)


def rgb_plot_settings():
    ax = plt.gca()
    ax.tick_params(colors='black', width=0.3, length=1.5, pad=2)
    ax.set_facecolor('#F4F4F4')
    plt.grid(color='white', linewidth=0.3, linestyle='solid')
    ax.set_axisbelow(True)
    plt.xticks(ticks=[0, 32, 64, 96, 128, 160, 192, 224, 255], labels=[0, 32, 64, 96, 128, 160, 192, 224, 255])
    ax.set_xlim([0, 255])


def get_rgb_plots(file) -> list[str]:
    image = Image.open(file)
    pixels = image.load()
    rgb = [[0 for _ in range(256)] for _ in range(3)]
    for i in range(image.width):
        for j in range(image.height):
            for k in range(3):
                rgb[k][pixels[i, j][k]] += 1

    plots = []
    for k in range(3):
        fig = plt.figure(figsize=(4, 2), dpi=300)
        plt.bar([i for i in range(256)], rgb[k], width=1, color='#4285f4')
        rgb_plot_settings()
        plots.append(get_plot_as_string(fig))

    return plots


def get_luminosity_plot(file) -> str:
    image = Image.open(file)
    pixels = image.load()

    luminosity = {}
    for i in range(image.width):
        for j in range(image.height):
            rgb = pixels[i, j]
            y = round(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            if y in luminosity:
                luminosity[y] += 1
            else:
                luminosity[y] = 1

    fig = plt.figure(figsize=(4, 2), dpi=300)
    plt.bar(luminosity.keys(), luminosity.values(), width=1, color='#4285f4')
    rgb_plot_settings()

    return get_plot_as_string(fig)


def rgb_to_linear(rgb):
    for i in range(3):
        rgb[i] /= 255
        if rgb[i] < 0.04045:
            rgb[i] /= 12.92
        else:
            rgb[i] = ((rgb[i] + 0.055) / 1.055) ** 2.4
    return rgb
