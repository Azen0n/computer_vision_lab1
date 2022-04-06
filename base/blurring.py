import math
from multiprocessing import Pool

from PIL import Image, ImageDraw
import numpy as np


def square_filter(image: Image, kernel_size: int) -> Image:
    """2.1. Прямоугольный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')
    kernel_radius = int(kernel_size / 2)

    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = np.zeros((image.height, image.width))
    for j in range(image.width - kernel_size + 1):
        for i in range(image.height - kernel_size + 1):
            kernel_pixels = pixels[i:i + kernel_size, j:j + kernel_size]
            new_pixels[i + kernel_radius, j + kernel_radius] = int(np.mean(kernel_pixels))
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')

    return new_image


def median_filter(image: Image, kernel_size: int) -> str:
    """2.1. Медианный фильтр с размерами ядра 3x3 или 5x5."""
    if kernel_size not in [3, 5]:
        raise ValueError('Kernel size must be either 3 or 5.')
    kernel_radius = int(kernel_size / 2)

    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = np.zeros((image.height, image.width))
    for j in range(image.width - kernel_size + 1):
        for i in range(image.height - kernel_size + 1):
            kernel_pixels = pixels[i:i + kernel_size, j:j + kernel_size]
            new_pixels[i + kernel_radius, j + kernel_radius] = int(np.median(kernel_pixels))
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')

    return new_image


def gaussian_filter(image: Image, sigma: float) -> str:
    """2.2. Фильтр Гаусса."""
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    kernel_radius = int(np.ceil(3 * sigma) - 1)
    kernel_size = int(kernel_radius * 2 + 1)
    filter_ = get_gaussian_filter(sigma)
    new_pixels = np.zeros((image.height, image.width))
    for j in range(image.width - kernel_size + 1):
        for i in range(image.height - kernel_size + 1):
            kernel_pixels = pixels[i:i + kernel_size, j:j + kernel_size]
            new_pixels[i + kernel_radius, j + kernel_radius] = int(np.sum(filter_ * kernel_pixels))
    new_image = Image.fromarray(np.uint8(new_pixels), 'L')

    return new_image


def get_gaussian_filter(sigma: float):
    kernel_radius = int(np.ceil(3 * sigma) - 1)
    kernel_size = int(2 * kernel_radius + 1)
    filter_ = np.zeros((kernel_size, kernel_size))
    for i in range(kernel_size):
        for j in range(kernel_size):
            filter_[i][j] = math.exp(-((i - kernel_radius) ** 2 + (j - kernel_radius) ** 2) / (2 * sigma * sigma))
    return np.array(filter_ / np.sum(filter_))


def sigma_filter(image: Image, sigma: float, kernel_size: int) -> str:
    """2.3. Сигма-фильтр."""
    kernel_radius = int(kernel_size / 2)

    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    new_pixels = np.zeros((image.height, image.width))
    for j in range(image.width - kernel_size + 1):
        for i in range(image.height - kernel_size + 1):
            kernel_pixels = pixels[i:i + kernel_size, j:j + kernel_size]
            center = kernel_pixels[kernel_radius, kernel_radius]
            pixels_in_range = np.logical_and(kernel_pixels >= center - sigma, kernel_pixels <= center + sigma)
            new_pixels[i + kernel_radius, j + kernel_radius] = int(np.mean(kernel_pixels[pixels_in_range]))
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
