import base64
import io
import random
import urllib

from PIL import Image, ImageDraw
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


def flip_horizontally(file) -> str:
    image = Image.open(file)
    pixels = image.load()
    new_image = Image.new('RGB', image.size)
    draw = ImageDraw.Draw(new_image)
    for i in range(image.width):
        for j in range(image.height):
            draw.point((i, image.height - 1 - j), (pixels[i, j]))

    return image_to_string(new_image)


def flip_vertically(file) -> str:
    image = Image.open(file)
    pixels = image.load()
    new_image = Image.new('RGB', image.size)
    draw = ImageDraw.Draw(new_image)
    for i in range(image.width):
        for j in range(image.height):
            draw.point((image.width - 1 - i, j), (pixels[i, j]))

    return image_to_string(new_image)


def image_to_string(image: Image) -> str:
    with io.BytesIO() as output:
        image.save(output, format='png')
        content = output.getvalue()

    return 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(content))


def is_in_image(x: int, y: int, image: Image) -> bool:
    return 0 <= x < image.width and 0 <= y < image.height


def get_eight_blur_pixels(x: int, y: int, image: Image, pixels) -> list[tuple[int, int, int]]:
    blur_pixels = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_in_image(x + i, y + j, image):
                blur_pixels.append(pixels[(x + i, y + j)])
    return blur_pixels


def get_four_blur_pixels(x: int, y: int, image: Image, pixels) -> list[tuple[int, int, int]]:
    blur_pixels = []
    blur_pixels_coordinates = [(x, y + 1), (x - 1, y), (x, y), (x + 1, y), (x, y - 1)]
    for coordinates in blur_pixels_coordinates:
        if is_in_image(*coordinates, image):
            blur_pixels.append(pixels[coordinates])
    return blur_pixels


def blur(file, number_of_blur_pixels: int) -> str:
    image = Image.open(file)
    pixels = image.load()
    new_image = Image.new('RGB', image.size)
    draw = ImageDraw.Draw(new_image)

    if number_of_blur_pixels == 4:
        get_blur_pixels = get_four_blur_pixels
    else:
        get_blur_pixels = get_eight_blur_pixels

    for i in range(image.width):
        for j in range(image.height):
            blur_pixels = get_blur_pixels(i, j, image, pixels)
            rgb_values = [[color_values] for color_values in zip(*blur_pixels)]
            mean_rgb_value = tuple(round(sum(color_values[0]) / len(color_values[0]))
                                   for color_values in rgb_values)
            draw.point((i, j), mean_rgb_value)

    return image_to_string(new_image)
