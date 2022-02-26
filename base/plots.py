import base64
import io
import random
import urllib
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw

imageMain = None


def get_plot(max_value: int) -> str:
    if type(max_value) != int:
        max_value = int(max_value)
    x = [i + 1 for i in range(max_value)]
    y = []
    y_value = 0
    for i in range(max_value):
        y_value += random.randint(-10, 10)
        y.append(y_value)

    fig = plt.figure()
    plt.plot(x, y)

    return get_plot_as_string(fig)


def get_plot_as_string(fig: plt.Figure) -> str:
    """Превращает изображение графика в строку."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return 'data:image/png;base64,' + urllib.parse.quote(string)


def get_name_plot() -> str:
    fig = plt.figure()

    # График создавать тут
    plt.plot([100, 20, 30, 40, 50], [1, 2, 3, 4, 5])

    return get_plot_as_string(fig)


def checkingRange(x, y, width, height):
    if (x >= 0 and x < width):
        if (y >= 0 and y < height):
            return True
    return False


def removeNoise(image, type):
    """5.6"""
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    if type == 8:
        for i in range(width):
            for j in range(height):
                p = []
                if (checkingRange(i, j, width, height)):
                    p.append(pix[i, j])
                if (checkingRange(i + 1, j + 1, width, height)):
                    p.append(pix[i + 1, j + 1])
                if (checkingRange(i + 1, j, width, height)):
                    p.append(pix[i + 1, j])
                if (checkingRange(i + 1, j - 1, width, height)):
                    p.append(pix[i + 1, j - 1])
                if (checkingRange(i, j - 1, width, height)):
                    p.append(pix[i, j - 1])
                if (checkingRange(i - 1, j - 1, width, height)):
                    p.append(pix[i - 1, j - 1])
                if (checkingRange(i - 1, j, width, height)):
                    p.append(pix[i - 1, j])
                if (checkingRange(i - 1, j + 1, width, height)):
                    p.append(pix[i - 1, j + 1])
                if (checkingRange(i, j + 1, width, height)):
                    p.append(pix[i, j + 1])

                rgb = [0, 0, 0]
                l = len(p)
                for x in p:
                    rgb[0] += x[0]
                    rgb[1] += x[1]
                    rgb[2] += x[2]
                rgb[0] /= l
                rgb[1] /= l
                rgb[2] /= l
                draw.point((i, j), (round(rgb[0]), round(rgb[1]), round(rgb[2])))
    if type == 4:
        for i in range(width):
            for j in range(height):
                p = []
                if (checkingRange(i, j, width, height)):
                    p.append(pix[i, j])
                if (checkingRange(i + 1, j, width, height)):
                    p.append(pix[i + 1, j])
                if (checkingRange(i, j - 1, width, height)):
                    p.append(pix[i, j - 1])
                if (checkingRange(i - 1, j, width, height)):
                    p.append(pix[i - 1, j])
                if (checkingRange(i, j + 1, width, height)):
                    p.append(pix[i, j + 1])
                rgb = [0, 0, 0]
                l = len(p)
                for x in p:
                    rgb[0] += x[0]
                    rgb[1] += x[1]
                    rgb[2] += x[2]
                rgb[0] /= l
                rgb[1] /= l
                rgb[2] /= l
                draw.point((i, j), (round(rgb[0]), round(rgb[1]), round(rgb[2])))

def changingBrightness(image,value,channel):
    """5.1"""
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    if (channel == 3):
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0] + value
                b = pix[i, j][1] + value
                c = pix[i, j][2] + value
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
    elif channel == 2:
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2] + value
                if (c < 0):
                    c = 0
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
    elif channel == 1:
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1] + value
                c = pix[i, j][2]
                if (b < 0):
                    b = 0
                if (b > 255):
                    b = 255
                draw.point((i, j), (a, b, c))
    elif channel == 0:
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0] + value
                b = pix[i, j][1]
                c = pix[i, j][2]
                if (a < 0):
                    a = 0
                if (a > 255):
                    a = 255
                draw.point((i, j), (a, b, c))


def get_chart_plot(image, color) -> str:
    """2 пункт"""
    fig = plt.figure()
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    if (color != 3):
        cnt = dict()
        for i in range(256):
            cnt[i] = 0
        for x in range(width):
            for y in range(height):
                r = pix[x, y][color]
                cnt[r] += 1
    else:
        cnt = dict()
        for i in range(256):
            cnt[i] = 0
        for x in range(width):
            for y in range(height):
                r = pix[x, y][0]
                g = pix[x, y][1]
                b = pix[x, y][2]
                y = round(0.3 * r + 0.59 * g + 0.11 * b)
                cnt[y] += 1
    x = cnt.keys()
    y = cnt.values()
    plt.bar(x, y, width=1)
    return get_plot_as_string(fig)


def verticalDisplay():
    """5.5 пункт
        Надо передавать image
        или брать imMain
        а также вернуть картинку"""
    image = Image.open("C:/Users/Aoki/Pictures/Screenshots/5.png")  # Открываем изображение.
    pix = image.load()
    width = image.size[0]
    height = image.size[1]
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    for i in range(width):
        for j in range(height):
            draw.point((width - 1 - i, j), (pix[i, j]))
    im.show()


def horizontalDisplay():
    """5.5 пункт"""
    image = Image.open("C:/Users/Aoki/Pictures/Screenshots/5.png")  # Открываем изображение.
    pix = image.load()
    width = image.size[0]
    height = image.size[1]
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    for i in range(width):
        for j in range(height):
            draw.point((i, height - 1 - j), (pix[i, j]))
    im.show()


def channelExchange(color1, color2):
    """5.4 пункт"""
    image = Image.open("C:/Users/Aoki/Pictures/Screenshots/22.png")  # Открываем изображение.
    pix = image.load()
    width = image.size[0]
    height = image.size[1]
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    if ((color1 == 0 and color2 == 1) or (color1 == 1 and color2 == 0)):
        for i in range(width):
            for j in range(height):
                r = pix[i, j][1]
                g = pix[i, j][0]
                b = pix[i, j][2]
                draw.point((i, j), (r, g, b))
    elif ((color1 == 0 and color2 == 2) or (color1 == 2 and color2 == 0)):
        for i in range(width):
            for j in range(height):
                r = pix[i, j][2]
                g = pix[i, j][1]
                b = pix[i, j][0]
                draw.point((i, j), (r, g, b))
    elif ((color1 == 1 and color2 == 2) or (color1 == 2 and color2 == 1)):
        for i in range(width):
            for j in range(height):
                r = pix[i, j][0]
                g = pix[i, j][2]
                b = pix[i, j][1]
                draw.point((i, j), (r, g, b))
    im.show()
