from PIL import Image
import numpy as np

from base.lab2.parallel_methods.gaussian_filter import p_gaussian_filter
from base.lab2.parallel_methods.sigma_filter import p_sigma_filter
from base.lab2.parallel_methods.median_filter import p_median_filter
from base.lab2.parallel_methods.square_filter import p_square_filter


def square_filter(image: Image, kernel_size: int) -> Image:
    """2.1. Прямоугольный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')

    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = p_square_filter(pixels, kernel_size)
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')

    return new_image


def median_filter(image: Image, kernel_size: int) -> str:
    """2.1. Медианный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')

    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = p_median_filter(pixels, kernel_size)
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')

    return new_image


def gaussian_filter(image: Image, sigma: float) -> str:
    """2.2. Фильтр Гаусса."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = p_gaussian_filter(pixels, sigma)
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')

    return new_image


def sigma_filter(image: Image, sigma: float, kernel_size: int) -> str:
    """2.3. Сигма-фильтр."""

    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = p_sigma_filter(pixels, sigma, kernel_size)
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')
    return new_image
