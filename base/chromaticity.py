from PIL import Image
import numpy as np


def forward_log(image: Image) -> Image:
    """1.1. Прямое логарифмическое преобразование."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    pixels = 60 * np.log(1 + pixels)
    pixels[pixels > 255] = 255
    new_image = Image.fromarray(np.uint8(pixels), 'L')

    return new_image


def backward_log(image: Image) -> Image:
    """1.1. Обратное логарифмическое преобразование."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    pixels = np.exp(pixels) ** (1 / 60) - 1
    new_image = Image.fromarray(np.uint8(pixels), 'L')

    return new_image


def power_law(image: Image, gamma: int) -> Image:
    """1.2. Степенное преобразование."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    pixels = (pixels / 255) ** (1 / gamma) * 255
    new_image = Image.fromarray(np.uint8(pixels), 'L')

    return new_image


def binary(image: Image, threshold: int) -> Image:
    """1.3. Бинарное преобразование с произвольным пороговым значением."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    pixels[pixels > threshold] = 255
    pixels[pixels < threshold] = 0
    new_image = Image.fromarray(np.uint8(pixels), 'L')

    return new_image


def bit_plane_slicing(image: Image, bit: int) -> Image:
    """1.4. Вырезание произвольной битовой плоскости."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    bit_pixels = np.zeros((image.height, image.width))
    for i in range(image.height):
        for j in range(image.width):
            bit_pixels[i, j] = 255 * int(np.binary_repr(pixels[i, j], 8)[8 - bit])
    new_image = Image.fromarray(np.uint8(bit_pixels), 'L')

    return new_image


def cutting_out_intensity_range(image: Image, start: int, end: int, constant_value: int = None) -> Image:
    """1.5. Вырезание произвольного диапазона [start, end] яркостей.

    1.5.2. Если constant_value равно None, все пиксели вне диапазона остаются в исходном виде,
    1.5.1. иначе заменет их значение на constant_value.
    """
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    pixels_in_range = np.logical_and(pixels >= start, pixels <= end)
    pixels[pixels_in_range] = 255
    if constant_value is not None:
        pixels[~pixels_in_range] = constant_value
    new_image = Image.fromarray(np.uint8(pixels), 'L')

    return new_image
