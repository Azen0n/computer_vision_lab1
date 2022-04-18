import copy

from PIL import Image, ImageDraw


def sobel_kernel(kernel_size: int):
    kernel_radius = int(kernel_size / 2)
    kernel_x = [[0 for _ in range(kernel_size)] for _ in range(kernel_size)]
    kernel_y = copy.deepcopy(kernel_x)
    coefficient = 2 if kernel_size == 3 else 20 if kernel_size == 5 else 780

    for i in range(-kernel_radius, kernel_radius + 1):
        for j in range(-kernel_radius, kernel_radius + 1):
            if i == j == 0:
                kernel_x[i - kernel_radius][j - kernel_radius] = 0
                kernel_y[i - kernel_radius][j - kernel_radius] = 0
            else:
                kernel_x[i - kernel_radius][j - kernel_radius] = int(j / (i * i + j * j) * coefficient)
                kernel_y[i - kernel_radius][j - kernel_radius] = int(i / (i * i + j * j) * coefficient)
    return kernel_x, kernel_y


def sobel(image: Image, kernel_size: int) -> Image:
    """1. Фильтр Собеля с размером ядра 3x3, 5x5 и 7x7."""
    kernel_radius = int(kernel_size / 2)
    image = image.convert("L")
    new_image = Image.new("L", image.size)
    pix = image.load()
    draw = ImageDraw.Draw(new_image)
    kernel_x, kernel_y = sobel_kernel(kernel_size)
    for y in range(kernel_radius, image.height - kernel_radius):
        for x in range(kernel_radius, image.width - kernel_radius):
            gradient_x = 0
            gradient_y = 0
            for i in range(-kernel_radius, kernel_radius + 1):
                for j in range(-kernel_radius, kernel_radius + 1):
                    gradient_x += pix[x + i, y + j] * kernel_x[kernel_radius + i][kernel_radius + j]
                    gradient_y += pix[x + i, y + j] * kernel_y[kernel_radius + i][kernel_radius + j]
            draw.point((x, y), round((gradient_x ** 2 + gradient_y ** 2) ** 0.5))

    return new_image
