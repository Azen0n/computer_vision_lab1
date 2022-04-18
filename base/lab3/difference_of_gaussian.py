from PIL import Image, ImageDraw
from base.lab2.blurring import gaussian_filter


def difference_of_gaussian(image: Image, coefficient: float, sigma: float) -> Image:
    """2.2. Метод DoG для распознавания границ."""
    higher = gaussian_filter(image, coefficient * sigma)
    lower = gaussian_filter(image, sigma)
    higher_pixels = higher.load()
    lower_pixels = lower.load()

    new_image = Image.new('L', image.size)
    draw = ImageDraw.Draw(new_image)

    for i in range(image.width):
        for j in range(image.height):
            draw.point((i, j), 5 * (higher_pixels[i, j] - lower_pixels[i, j]))

    return new_image
