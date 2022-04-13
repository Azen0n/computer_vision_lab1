from PIL import Image
import numpy as np

from base.parallel_methods.gaussian_filter import p_gaussian_filter
from base.parallel_methods.sigma_filter import p_sigma_filter
from base.parallel_methods.median_filter import p_median_filter
from base.parallel_methods.square_filter import p_square_filter


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


def is_in_image(x: int, y: int, image: Image) -> bool:
    if 0 <= x < image.width and 0 <= y < image.height:
        return True
    else:
        return False


def get_kernel_pixels(pix, x: int, y: int, kernel_radius: int, image: Image) -> list:
    kernel_pixels = []
    for i in range(x - kernel_radius, x + kernel_radius + 1):
        for j in range(y - kernel_radius, y + kernel_radius + 1):
            if is_in_image(i, j, image):
                kernel_pixels.append(pix[i, j])
    return kernel_pixels


def get_filtered_kernel_pixels(pix, x: int, y: int, kernel_radius: int, filter_: list, image: Image) -> list:
    filtered_kernel_pixels = []
    kernel_size = 2 * kernel_radius + 1
    for i in range(kernel_size):
        for j in range(kernel_size):
            if is_in_image(x + i - kernel_radius, y + j - kernel_radius, image):
                filtered_kernel_pixels.append(filter_[i][j] * pix[x + i - kernel_radius, y + j - kernel_radius])
    return filtered_kernel_pixels


def truncate_pixel(pixel: int) -> int:
    if pixel < 0:
        return 0
    elif pixel > 255:
        return 255
    return pixel
