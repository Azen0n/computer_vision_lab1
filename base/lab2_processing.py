import base64
import io
import math
from urllib.parse import quote

from PIL import Image, ImageDraw
import numpy as np

import base.chromaticity as chroma
import base.blurring as blur


def get_image_as_string(image: Image) -> str:
    """Превращает изображение в строку с HTML тегами."""
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        contents = output.getvalue()

    return 'data:image/png;base64,' + quote(base64.b64encode(contents))


def delta(first_image: Image, second_image: Image) -> float:
    first_image = first_image.convert('L')
    second_image = second_image.convert('L')
    first_image_pixels = np.asarray(first_image)
    second_image_pixels = np.asarray(second_image)
    diff = first_image_pixels - second_image_pixels
    return np.sum(diff) / (first_image.width * first_image.height)


def mean_absolute_error(first_image: Image, second_image: Image) -> float:
    first_image = first_image.convert('L')
    second_image = second_image.convert('L')
    first_image_pixels = np.asarray(first_image)
    second_image_pixels = np.asarray(second_image)
    diff = np.absolute(first_image_pixels - second_image_pixels)
    return np.sum(diff) / (first_image.width * first_image.height)


def mean_squared_error(first_image: Image, second_image: Image) -> float:
    first_image = first_image.convert('L')
    second_image = second_image.convert('L')
    first_image_pixels = np.asarray(first_image)
    second_image_pixels = np.asarray(second_image)
    diff = np.power(first_image_pixels - second_image_pixels, 2)
    return np.sum(diff) / (first_image.width * first_image.height)


def unsharp_masking(image: Image, contrast_percent: int, blur_method_name: str, sigma: int, kernel_size: int = None) -> Image:
    """3.1. Нерезкое маскирование для повышения резкости изображения."""
    blur_method = methods[blur_method_name]
    if kernel_size is None:
        blurred_image = blur_method(image, sigma)
    else:
        blurred_image = blur_method(image, sigma, kernel_size)

    image_pixels = np.asarray(image.convert('L')).astype(int)
    blurred_image_pixels = np.asarray(blurred_image).astype(int)
    diff = image_pixels - blurred_image_pixels

    new_image_pixels = image_pixels + contrast_percent * diff
    new_image = Image.fromarray(np.uint8(new_image_pixels), 'L')

    return new_image


def noise(image: Image) -> Image:
    image = image.convert('L')
    pixels = np.asarray(image).astype(int)
    noise_mask = np.random.random((image.height, image.width))
    noise_mask[noise_mask > 0.95] = 255
    noise_mask[noise_mask != 255] = 0
    new_pixels = pixels - noise_mask
    new_pixels[new_pixels < 0] = 0

    return Image.fromarray(np.uint8(new_pixels), 'L')


methods = {
    'log': chroma.forward_log,
    'backward_log': chroma.backward_log,
    'power_law': chroma.power_law,
    'binary': chroma.binary,
    'bit_plane_slicing': chroma.bit_plane_slicing,
    'cutting_out_intensity_range': chroma.cutting_out_intensity_range,
    'square_filter': blur.square_filter,
    'median_filter': blur.median_filter,
    'gaussian_filter': blur.gaussian_filter,
    'sigma_filter': blur.sigma_filter,
    'unsharp_masking': unsharp_masking,
    'noise': noise,
}
