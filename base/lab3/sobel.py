from PIL import Image, ImageDraw
import numpy as np
from scipy.signal import convolve2d


def custom_sobel(shape, axis):
    if (shape[0] not in [3, 5, 7]):
        return 0
    else:
        cof = 2 if shape[0] == 3 else 20 if shape[0] == 5 else 780
        k = np.zeros(shape)
        p = [(j, i) for j in range(shape[0])
             for i in range(shape[1])
             if not (i == (shape[1] - 1) / 2. and j == (shape[0] - 1) / 2.)]

        for j, i in p:
            j_ = int(j - (shape[0] - 1) / 2.)
            i_ = int(i - (shape[1] - 1) / 2.)
            k[j, i] = (i_ if axis == 0 else j_) / float(i_ * i_ + j_ * j_)
    return k * cof


def sobel(image: Image, kernel_size: int) -> Image:
    """1. Фильтр Собеля с размером ядра 3x3, 5x5 и 7x7."""
    """Для 5 и 7 работает плохо. Фильтр правильный хз в чем дело."""
    kernel_radius = int(kernel_size / 2)
    height = image.size[1]
    weight = image.size[0]
    im = Image.new("L", (weight, height))
    pix = image.load()
    draw = ImageDraw.Draw(im)
    sobel_x = custom_sobel((kernel_size, kernel_size), 0)
    sobel_y = custom_sobel((kernel_size, kernel_size), 1)
    for y in range(kernel_radius, height - kernel_radius):
        for x in range(kernel_radius, weight - kernel_radius):
            gradient_x = 0
            gradient_y = 0
            for x_ in range(-kernel_radius, kernel_radius + 1):
                for y_ in range(-kernel_radius, kernel_radius + 1):
                    gradient_x += pix[x + x_, y + y_] * sobel_x[kernel_radius + x_][kernel_radius + y_]
                    gradient_y += pix[x + x_, y + y_] * sobel_y[kernel_radius + x_][kernel_radius + y_]
            draw.point((x, y), round(pow(pow(gradient_y, 2) + pow(gradient_x, 2), 1 / 2)))
    im.show()


path = "./Screenshot 2022-04-17 181712.png"
image = Image.open(path)
image = image.convert("L")
height = image.size[1]
weight = image.size[0]
sobel(image, 3)
sobel(image, 5)
sobel(image, 7)
