import base64
import io
import random
import urllib
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
    plt.xticks(ticks=[0, 32, 64, 96, 128, 160, 192, 224, 255], labels=[0, 32, 64, 96, 128, 160, 192, 224, 255])
    ax.set_axisbelow(True)
    ax.set_xlim([0, 255])


def get_name_plot() -> str:
    fig = plt.figure(figsize=(4, 2), dpi=300)

    # График создавать тут
    plt.hist([random.randint(0, 255) for _ in range(400 * 600)], 255, color='#4285f4')
    rgb_plot_settings()

    return get_plot_as_string(fig)
