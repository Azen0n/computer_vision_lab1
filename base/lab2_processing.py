import base64
import io
import math
from urllib.parse import quote

from PIL import Image, ImageDraw


def get_image_as_string(image: Image) -> str:
    """Превращает изображение графика в строку."""
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        contents = output.getvalue()

    return 'data:image/png;base64,' + quote(base64.b64encode(contents))


def forward_log(image) -> str:
    """1.1. Прямое логарифмическое преобразование."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for x in range(0, image.width):
        for y in range(0, image.height):
            new_p = 60 * math.log(1 + pix[x, y])
            draw.point((x, y), round(abs(new_p)))

    return get_image_as_string(new_image)


def backward_log(image) -> str:
    """1.1. Обратное логарифмическое преобразование."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for x in range(0, image.width):
        for y in range(0, image.height):
            new_p = (math.exp(pix[x, y]) ** (1 / 60)) - 1
            draw.point((x, y), round(abs(new_p)))

    return get_image_as_string(new_image)


def power_law(image, gamma):
    """1.2. Степенное преобразование."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for x in range(0, image.width):
        for y in range(0, image.height):  # 3 канала
            new_p = pow(pix[x, y] / 255, 1 / gamma) * 255
            draw.point((x, y), round(new_p))

    return get_image_as_string(new_image)


def binary(image, threshold):
    """1.3. Бинарное преобразование с произвольным пороговым значением."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            if pix[i, j] > threshold:
                draw.point((i, j), 255)
            else:
                draw.point((i, j), 0)

    return get_image_as_string(new_image)


def bit_plane_slicing(image, bit):
    """1.4. Вырезание произвольной битовой плоскости."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            bit_pix = format(pix[i, j], 'b')
            if len(bit_pix) < 8:
                bit_pix = '0' * (8 - len(bit_pix)) + bit_pix
            bit_pix = int(bit_pix[len(bit_pix) - bit])
            draw.point((i, j), bit_pix * 255)

    return get_image_as_string(new_image)


# 1.5. Вырезание произвольного диапазона яркостей.
# 1.5.1. Пиксели вне диапазона приведены к произвольному константному значению.
# 1.5.2. Пиксели вне диапазона сохранены в исходном виде.


def is_in_image(x, y, image):
    if 0 <= x < image.width and 0 <= y < image.height:
        return True
    else:
        return False


def square_filter(image, kernel_size):
    """2.1. Прямоугольный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')
    kernel_radius = int(kernel_size / 2)

    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            kernel_pixels = get_kernel_pixels(pix, i, j, kernel_radius, image)
            kernel_mean = round(sum(kernel_pixels) / len(kernel_pixels))
            draw.point((i, j), kernel_mean)

    return get_image_as_string(new_image)


def get_kernel_pixels(pix, x, y, kernel_radius, image):
    kernel_pixels = []
    for i in range(x - kernel_radius, x + kernel_radius + 1):
        for j in range(y - kernel_radius, y + kernel_radius + 1):
            if is_in_image(i, j, image):
                kernel_pixels.append(pix[i, j])
    return kernel_pixels


def median_filter(image, kernel_size):
    """2.1. Медианный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')
    kernel_radius = int(kernel_size / 2)

    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            kernel_pixels = get_kernel_pixels(pix, i, j, kernel_radius, image)
            kernel_pixels.sort()
            kernel_median = kernel_pixels[round(len(kernel_pixels) / 2)]
            draw.point((i, j), kernel_median)

    return get_image_as_string(new_image)


# 2.2. Фильтр Гаусса.
# 2.3. Сигма-фильтр.
# 2.4. Сравнение качества обработки зашумленного изображения.
# 2.4.1. delta
# 2.4.2. MSE
# 2.4.3. MSA

# 3.1. Нерезкое маскирование для повышения резкости изображения.
# 3.2. ???
# 3.3. ???


methods = {
    'log': forward_log,
    'backward_log': backward_log,
    'power_law': power_law,
    'binary': binary,
    'bit_plane_slicing': bit_plane_slicing,
    'square_filter': square_filter,
    'median_filter': median_filter,
}
