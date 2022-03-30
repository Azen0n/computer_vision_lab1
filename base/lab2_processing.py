import base64
import io
import math
import re
from urllib.parse import quote, unquote

from PIL import Image, ImageDraw


def get_image_as_string(image: Image) -> str:
    """Превращает изображение в строку с HTML тегами."""
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        contents = output.getvalue()

    return 'data:image/png;base64,' + quote(base64.b64encode(contents))


def forward_log(image: Image) -> str:
    """1.1. Прямое логарифмическое преобразование."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for x in range(0, image.width):
        for y in range(0, image.height):
            new_p = 60 * math.log(1 + pix[x, y])
            draw.point((x, y), round(abs(new_p)))

    return new_image


def backward_log(image: Image) -> str:
    """1.1. Обратное логарифмическое преобразование."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for x in range(0, image.width):
        for y in range(0, image.height):
            new_p = (math.exp(pix[x, y]) ** (1 / 60)) - 1
            draw.point((x, y), round(abs(new_p)))

    return new_image


def power_law(image: Image, gamma: int) -> str:
    """1.2. Степенное преобразование."""
    image = image.convert('L')
    new_image = Image.new('L', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for x in range(0, image.width):
        for y in range(0, image.height):  # 3 канала
            new_p = pow(pix[x, y] / 255, 1 / gamma) * 255
            draw.point((x, y), round(new_p))

    return new_image


def binary(image: Image, threshold: int) -> str:
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

    return new_image


def bit_plane_slicing(image: Image, bit: int) -> str:
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

    return new_image


def cutting_out_luma_range(image: Image, start: int, end: int, constant_value: int = None) -> str:
    """1.5. Вырезание произвольного диапазона [start, end] яркостей.

    1.5.2. Если constant_value равно None, все пиксели вне диапазона остаются в исходном виде,
    1.5.1. иначе заменет их значение на constant_value.
    """
    image = image.convert('RGB')
    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            luma = get_pixel_luma(pix[i, j])
            if round(luma) in range(start, end + 1):
                draw.point((i, j), (255, 255, 255))
            else:
                if constant_value is None:
                    draw.point((i, j), (pix[i, j]))
                else:
                    draw.point((i, j), (constant_value, constant_value, constant_value))

    return new_image


def get_pixel_luma(pixel) -> float:
    """Kind of luminosity — https://en.wikipedia.org/wiki/Luma_(video)."""
    return 0.3 * pixel[0] + 0.59 * pixel[1] + 0.11 * pixel[2]


def is_in_image(x: int, y: int, image: Image) -> bool:
    if 0 <= x < image.width and 0 <= y < image.height:
        return True
    else:
        return False


def square_filter(image: Image, kernel_size: int) -> str:
    """2.1. Прямоугольный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')
    kernel_radius = int(kernel_size / 2)

    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            kernel_pixels = get_kernel_pixels(pix, i, j, kernel_radius, image)
            sum_ = [0, 0, 0]
            for pixel in kernel_pixels:
                for k in range(3):
                    sum_[k] += pixel[k]

            kernel_mean = tuple([round(sum_[i] / len(kernel_pixels)) for i in range(3)])
            draw.point((i, j), kernel_mean)

    return new_image


def get_kernel_pixels(pix, x: int, y: int, kernel_radius: int, image: Image) -> list:
    kernel_pixels = []
    for i in range(x - kernel_radius, x + kernel_radius + 1):
        for j in range(y - kernel_radius, y + kernel_radius + 1):
            if is_in_image(i, j, image):
                kernel_pixels.append(pix[i, j])
    return kernel_pixels


def median_filter(image: Image, kernel_size: int) -> str:
    """2.1. Медианный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')
    kernel_radius = int(kernel_size / 2)

    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    for i in range(image.width):
        for j in range(image.height):
            kernel_pixels = get_kernel_pixels(pix, i, j, kernel_radius, image)
            kernel_pixels.sort()
            kernel_median = kernel_pixels[round(len(kernel_pixels) / 2)]
            draw.point((i, j), kernel_median)

    return new_image


def gaussian_filter(image: Image, sigma: float) -> str:
    """2.2. Фильтр Гаусса."""
    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()

    kernel_radius = math.ceil(3 * sigma)
    filter_ = get_filter(sigma)
    for i in range(image.width):
        for j in range(image.height):
            filtered_kernel_pixels = get_filtered_kernel_pixels(pix, i, j, kernel_radius, filter_, image)
            sum_ = [0, 0, 0]
            for pixel in filtered_kernel_pixels:
                for k in range(3):
                    sum_[k] += pixel[k]
            draw.point((i, j), tuple(truncate_pixel([round(sum_[i]) for i in range(3)])))

    return new_image


def get_filtered_kernel_pixels(pix, x: int, y: int, kernel_radius: int, filter_: list, image: Image) -> list:
    filtered_kernel_pixels = []
    kernel_size = 2 * kernel_radius + 1
    for i in range(kernel_size):
        for j in range(kernel_size):
            if is_in_image(x + i - kernel_radius, y + j - kernel_radius, image):
                pixel = []
                for k in range(3):
                    pixel.append(filter_[i][j] * pix[x + i - kernel_radius, y + j - kernel_radius][k])
                filtered_kernel_pixels.append(tuple(pixel))
    return filtered_kernel_pixels


def truncate_pixel(pixel: list[int]) -> list:
    new_pixel = [0, 0, 0]
    for i in range(3):
        if pixel[i] < 0:
            new_pixel[i] = 0
        elif pixel[i] > 255:
            new_pixel[i] = 255
        else:
            new_pixel[i] = pixel[i]
    return new_pixel


def get_filter(sigma: float):
    kernel_radius = math.ceil(3 * sigma)
    kernel_size = 2 * kernel_radius + 1
    filter_ = [[] for _ in range(kernel_size)]
    sum_ = 0
    for i in range(kernel_size):
        for j in range(kernel_size):
            gaussian = math.exp(-((i - kernel_radius) ** 2 + (j - kernel_radius) ** 2) / (2 * sigma * sigma))
            filter_[i].append(gaussian)
            sum_ += gaussian
    for i in range(kernel_size):
        for j in range(kernel_size):
            filter_[i][j] /= sum_
    return filter_


def sigma_filter(image: Image, sigma: float) -> str:
    """2.3. Сигма-фильтр."""
    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()
    kernel_radius = math.ceil(3 * sigma)
    for i in range(image.width):
        for j in range(image.height):
            kernel_pixels = get_kernel_pixels(pix, i, j, kernel_radius, image)

            valid_pixels = []
            for pixel in kernel_pixels:
                if lfdggkjkldjklgjdkgjkdjghkd(pix[i, j], pixel, sigma):
                    valid_pixels.append(pixel)

            sum_ = [0, 0, 0]
            for pixel in valid_pixels:
                for k in range(3):
                    sum_[k] += pixel[k]
            draw.point((i, j), tuple(truncate_pixel([round(sum_[i] / len(valid_pixels)) for i in range(3)])))

    return new_image


def lfdggkjkldjklgjdkgjkdjghkd(sgdf, sdfg, jjdsjd):
    new_sgdf1 = []
    for i in range(3):
        new_sgdf1.append(sgdf[i] - jjdsjd)
    new_sgdf2 = []
    for i in range(3):
        new_sgdf2.append(sgdf[i] + jjdsjd)
    return new_sgdf1[0] < sdfg[0] < new_sgdf2[0] and new_sgdf1[1] < sdfg[1] < new_sgdf2[1] and new_sgdf1[2] < sdfg[2] < new_sgdf2[2]


def mean_absolute_error(first_image: Image, second_image: Image) -> float:
    first_image_pixels = first_image.load()
    second_image_pixels = second_image.load()
    sum_ = 0
    for i in range(first_image.width):
        for j in range(first_image.height):
            sum_ += abs(first_image_pixels[i, j] - second_image_pixels[i, j])
    return sum_ / (first_image.width * first_image.height)


def mean_squared_error(first_image: Image, second_image: Image) -> float:
    first_image_pixels = first_image.load()
    second_image_pixels = second_image.load()
    sum_ = 0
    for i in range(first_image.width):
        for j in range(first_image.height):
            sum_ += (first_image_pixels[i, j] - second_image_pixels[i, j]) ** 2
    return sum_ / (first_image.width * first_image.height)


# 2.4. Сравнение качества обработки зашумленного изображения.


def unsharp_masking1(image: Image, contrast_percent: int, blur_method_name: str, sigma: float) -> str:
    """3.1. Нерезкое маскирование для повышения резкости изображения."""
    blur_method = methods[blur_method_name]
    blurred_image = blur_method(image, sigma)
    unsharp_mask = subtract_images(image, blurred_image)

    contrast_image = contrast(image, contrast_percent)
    contrast_pixels = contrast_image.load()
    original_pixels = image.load()

    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)

    for i in range(image.width):
        for j in range(image.height):
            original_color = original_pixels[i, j]
            contrast_color = contrast_pixels[i, j]
            luma_rate = 1 + get_pixel_luma(unsharp_mask[i][j]) / 255

            delta = []
            for k in range(3):
                difference = contrast_color[k] - original_color[k]
                delta.append(int(difference * luma_rate))
            new_color = truncate_pixel([original_color[i] + delta[i] for i in range(3)])
            draw.point((i, j), tuple(new_color))

    return new_image


def subtract_images(first_image: Image, second_image: Image):
    """Возвращает двумерный массив с разницей в значениях пикселей."""
    first_image_pixels = first_image.load()
    second_image_pixels = second_image.load()

    difference = [[] for _ in range(first_image.width)]
    for i in range(first_image.width):
        for j in range(first_image.height):
            diff = []
            for k in range(3):
                diff.append(first_image_pixels[i, j][k] - second_image_pixels[i, j][k])
            difference[i].append(diff)

    return difference


def contrast(image: Image, percent: int) -> str:
    new_image = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(new_image)
    pix = image.load()

    for i in range(image.width):
        for j in range(image.height):
            new_pixel = change_pixel_contrast(pix[i, j], percent)
            draw.point((i, j), new_pixel)

    return new_image


def change_pixel_contrast(pixel: list[int], percent: int):
    new_pixel = []
    for i in range(len(pixel)):
        new_channel_value = int((1 + percent / 100) * (pixel[i] - 128) + 128)
        new_pixel.append(new_channel_value)
    return tuple(truncate_pixel(new_pixel))


def unsharp_masking(image: Image, contrast_percent: int, blur_method_name: str, sigma):

    cof = 1
    kernel = [[0, -1 * cof, 0],
              [-1 * cof, 5 * cof, -1 * cof],
              [0, -1 * cof, 0]]
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for x in range(width):
        for y in range(height):
            newR = 0
            newG = 0
            newB = 0
            for h in range(0, 3):
                for w in range(0, 3):
                    if is_in_image(x + h - 1, y + w - 1, image):
                        newR += kernel[h][w] * pix[x + h - 1, y + w - 1][0]
                        newG += kernel[h][w] * pix[x + h - 1, y + w - 1][1]
                        newB += kernel[h][w] * pix[x + h - 1, y + w - 1][2]
            draw.point((x, y), (round(newR), round(newG), round(newB)))

    return im


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
    'cutting_out_luma_range': cutting_out_luma_range,
    'gaussian_filter': gaussian_filter,
    'sigma_filter': sigma_filter,
    'unsharp_masking': unsharp_masking,
}
