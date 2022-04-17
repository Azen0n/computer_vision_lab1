from PIL import Image


def sobel(image: Image, kernel_size: int) -> Image:
    """1. Фильтр Собеля с размером ядра 3x3, 5x5 и 7x7."""
    kernel_radius = int(kernel_size / 2)
