import math

import numpy as np
from PIL import Image, ImageDraw
from base.lab2.blurring import gaussian_filter


def laplacian_of_gaussian(image: Image, size, sigma: float) -> Image:
    """2.1. Метод LoG для распознавания границ."""
    image = image.convert("L")
    im = Image.new("L", image.size)
    draw = ImageDraw.Draw(im)
    LoG = np.ndarray(shape=(size, size))
    kernel_radius = int(size / 2)
    for x in range(-kernel_radius, kernel_radius + 1):
        for y in range(-kernel_radius, kernel_radius + 1):
            LoG[kernel_radius + x][kernel_radius + y] = (-1 / (math.pi * pow(sigma, 4))) * (
                    1 - (pow(x, 2) + pow(y, 2)) / 2 * pow(sigma, 2)) * math.exp(
                -1 * ((pow(x, 2) + pow(y, 2)) / 2 * pow(sigma, 2))) * 480
    pix = image.load()
    for y in range(kernel_radius, image.height - kernel_radius):
        for x in range(kernel_radius, image.width - kernel_radius):
            sm = 0
            for i in range(-kernel_radius, kernel_radius + 1):
                for j in range(-kernel_radius, kernel_radius + 1):
                    sm += pix[x - i, y - j] * LoG[i][j]
            draw.point((x, y), round(sm))
    return im
