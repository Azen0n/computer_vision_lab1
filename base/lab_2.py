import cmath
import math
import multiprocessing
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt, font_manager
from plots import get_rgb_plots


def chekingB(x):
    if x < 0:
        return 0
    if x > 255:
        return 255
    return x


def checkingRange(x, y, width, height):
    if (x >= 0 and x < width):
        if (y >= 0 and y < height):
            return True
    return False


def rectangular_filter(r):
    image = Image.open("1.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for i in range(width):
        for j in range(height):
            sm = 0
            count = 0
            for k in range(i - r, i + r + 1):
                for l in range(j - r, j + r + 1):
                    if (checkingRange(k, l, width, height)):
                        sm += pix[k, l]
                        count += 1
            draw.point((i, j), round(sm / count))
    im.show()


def getGaussian(r, sigma):
    size = 2 * r + 1
    filter = [[] for i in range(size)]
    for i in range(0, size):
        filter[i] = [0 for i in range(size)]
    sum = 0
    for i in range(0, size):
        for j in range(0, size):
            filter[i][j] = math.exp(-((i - r) * (i - r) + (j - r) * (j - r)) / (2 * sigma * sigma))
            sum += filter[i][j]
    for i in range(0, size):
        for j in range(0, size):
            filter[i][j] /= sum
    return filter


def gaussian_filter(filter, r):
    image = Image.open("1.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for x in range(0, width):
        for y in range(0, height):
            sum = 0
            for h in range(0, 2 * r + 1):
                for w in range(0, 2 * r + 1):
                    if (checkingRange(x + h - r, y + w - r, width, height)):
                        sum += filter[h][w] * pix[x + h - r, y + w - r]
            draw.point((x, y), round(chekingB(sum)))
    im.show()


def get_original():
    image = Image.open("1.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    return image


def border(x, y, h, w):
    if (x == 0 or x == (w - 1)):
        return True
    if (y == 0 or y == (h - 1)):
        return True
    return False


def sigma_filter(r, sigma):
    image = Image.open("ish2.jpg")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    gistW = dict()
    image.show()
    for p in range(width):
        print((int)((p + 1) * 100 / width))
        for q in range(height):
            for i in range(256):
                gistW[i] = 0
            for k in range(p - r, p + r + 1):
                for l in range(q - r, q + r + 1):
                    if (checkingRange(k, l, width, height)):
                        a = pix[k, l]
                        gistW[a] += 1
            sr = 0
            cnt = 0
            for l in range(pix[p, q] - sigma, pix[p, q] + sigma):
                if l in gistW:
                    sr += gistW[l] * l
                    cnt += 1
            newPix = round(sr / cnt)
            draw.point((p, q), newPix)
    im.show()


def FD():
    image = Image.open("50.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()

    for p in range(width):
        print(p)
        for q in range(height):
            sum_image_pix = 0
            for m in range(width):
                for n in range(height):
                    sum_image_pix += pix[m, n] * (math.cos(2 * math.pi * m / width))  # -math.sin(2*math.pi*))
            newPix = round(chekingB(sum_image_pix))

            if (border(p, q, height, width)):
                draw.point((p, q), 100)
            else:

                draw.point((p, q), newPix)
    im.show()


def binary_conversion(r):
    image = Image.open("256.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for i in range(width):
        for j in range(height):
            if (pix[i, j] > r):
                draw.point((i, j), 255)
            else:
                draw.point((i, j), 0)
    im.show()


def bit_plane_slicing(b):
    image = Image.open("256.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for i in range(width):
        for j in range(height):
            bitPix = format(pix[i, j], "b")
            if (len(bitPix) < 8):
                bitPix = "0" * (8 - len(bitPix)) + bitPix
            bitPix = (int)(bitPix[len(bitPix) - b])
            draw.point((i, j), bitPix * 255)
    im.show()


def median_filter(r):
    image = Image.open("1.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    ran = round(pow(2 * r + 1, 2) / 2)
    for i in range(width):
        for j in range(height):
            arr = []
            for k in range(i - r, i + r + 1):
                for l in range(j - r, j + r + 1):
                    if (checkingRange(k, l, width, height)):
                        arr.append(pix[k, l])
            arr.sort()
            a = arr[round(len(arr) / 2)]
            draw.point((i, j), a)
    return im


def metric_delta(x, y):
    # x,y  - матрица пикселей
    # и тут я понял что у этой матрицы нельзя узнать размеры -__-
    # или скидывать сюда картинки и у них узнавать размеры либо матрицы с размерами в аргументы
    # Значение этой метрики представляет собой среднюю
    # разницу значения цвета в соответствующих точках изображения.
    width = x.size[0]
    height = x.size[1]
    x.show()
    y.show()
    PixX = x.load()
    Pixy = y.load()
    _sum = 0
    for i in range(width):
        for j in range(height):
            _sum += Pixy[i, j] - PixX[i, j]  # числа отриц больше 1 Хз должно ли быть от 0 до 1
    return (_sum + 1) / (width * height)


def metric_MSE(x, y):
    # Метрика зависит только от разницы оригинала и искажения, это L2-норма этой разницы.
    width = x.size[0]
    height = x.size[1]
    PixX = x.load()
    Pixy = y.load()
    _sum = 0
    for i in range(width):
        for j in range(height):
            _sum += pow(Pixy[i, j] - PixX[i, j], 2)
    return (_sum + 1) / (width * height)


def metric_MSAD(x, y):
    # Метрика зависит только от разницы оригинала и искажения, это L2-норма этой разницы.
    width = x.size[0]
    height = x.size[1]
    PixX = x.load()
    Pixy = y.load()
    _sum = 0
    for i in range(width):
        for j in range(height):
            _sum += abs(Pixy[i, j] - PixX[i, j])
    return (_sum + 1) / (width * height)


def blurry_masking():  # Ебать что это за метод. Охно работает
    # Ха если поставить 4 то остануться тольк оконтуры
    # если 5 то уже норм будет

    cof = 1
    kernel = [[0, -1 * cof, 0],
              [-1 * cof, 5 * cof, -1 * cof],
              [0, -1 * cof, 0]]
    image = Image.open("1.png")
    image = image.convert('RGB')
    image.show()
    width = image.size[0]
    height = image.size[1]
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for x in range(width):
        for y in range(height):
            newR = 0
            newG = 0
            newB = 0
            for h in range(0, 3):
                for w in range(0, 3):
                    if (checkingRange(x + h - 1, y + w - 1, width, height)):
                        newR += kernel[h][w] * pix[x + h - 1, y + w - 1][0]
                        newG += kernel[h][w] * pix[x + h - 1, y + w - 1][1]
                        newB += kernel[h][w] * pix[x + h - 1, y + w - 1][2]
            draw.point((x, y), (round(newR), round(newG), round(newB)))
    im.show()


def get_max_int(image):
    width = image.size[0]
    height = image.size[1]
    mx = 0
    pix = image.load()
    for x in range(0, width):
        for y in range(0, height):
            if (mx < pix[x, y]):
                mx = pix[x, y]
    return mx


def forward_logarithmic_transformation(c):
    image = Image.open("1.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    mx = get_max_int(image)
    import numpy as np
    for x in range(0, width):
        for y in range(0, height):
            # newP = c * math.log(1 + pix[x, y], 10)
            newP = 60 * np.log(1 + pix[x, y])
            # newPR = (math.exp(newP)**(1/60))-1
            # newP = pow(10,pix[x,y]/2)-1
            draw.point((x, y), round(abs(newP)))
    im.show()

    im.save("prm.png")


def forward_logarithmic_transformation2(gammat):
    image = Image.open("1.png")
    image = image.convert('L')
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    mx = get_max_int(image)
    import numpy as np
    for x in range(0, width):
        for y in range(0, height):  # 3 канала
            newP = pow(pix[x, y] / 255, 1 / gammat) * 255
            draw.point((x, y), round(newP))
    im.show()


import cmath
import numpy as np

def getbar(img):
    values = [0 for i in range(256)]
    x = [i for i in range(256)]
    M = img.size[0]
    N = img.size[1]
    pix = img.load()
    for i in range(M):
        for j in range(N):
            values[pix[i,j]] +=1
    plt.bar(x,values,alpha = 1)
    plt.show()

def direct_fourier_transform():
    image = Image.open("123123.jpg")
    image = image.convert('L')
    M = image.size[0]
    N = image.size[1]
    im = Image.new('L', (M, N))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    Wm = cmath.exp(-cmath.sqrt(-1) * 2 * math.pi / M)
    Wn = cmath.exp(-cmath.sqrt(-1) * 2 * math.pi / N)
    Em = np.zeros((M, M))
    En = np.zeros((N, N))
    Gm = np.zeros((M, M)) + Wm
    Gn = np.zeros((N, N)) + Wn
    F = np.zeros((M, N))
    pixNew = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            pixNew[i][j] = pix[i, j]

    for row in range(M - 1):
        for col in range(M - 1):
            Em[row + 1][col + 1] = (row * col)
            Gm[row + 1][col + 1] = pow(Gm[row + 1][col + 1], Em[row + 1][col + 1])
    for row in range(N - 1):
        for col in range(N - 1):
            En[row + 1][col + 1] = (row * col)
            Gn[row + 1][col + 1] = pow(Gn[row + 1][col + 1], En[row + 1][col + 1])
    F = np.dot(Gm, pixNew)
    F = np.dot(F, Gn)
    realF = (F).real
    imagF = (F).imag
    mx = np.max(realF)
    mx = mx
    mn = np.min(realF)
    for i in range(M):
        for j in range(N):
            # norm = 255*((realF[i][j]-mn)/(mx-mn))
            draw.point((i, j), round(realF[i][j]))
    # im.show()
    # plt.show()
    return F


def Pref(image):
    width = image.size[0]
    height = image.size[1]
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    for i in range(width):
        for j in range(height):
            draw.point((width - 1 - i, height - 1 - j), (255 - pix[i, j]))
    return im

def back_fourier_transform(f):
    image = Image.open("123123.jpg")
    image = image.convert('L')
    M = image.size[0]
    N = image.size[1]
    im = Image.new('L', (M, N))
    draw = ImageDraw.Draw(im)
    pix = image.load()
    Wm = cmath.exp(-cmath.sqrt(-1) * 2 * math.pi / M)
    Wn = cmath.exp(-cmath.sqrt(-1) * 2 * math.pi / N)
    Em = np.zeros((M, M))
    En = np.zeros((N, N))
    Gm = np.zeros((M, M)) + Wm
    Gn = np.zeros((N, N)) + Wn
    F = np.zeros((M, N))
    pixNew = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            pixNew[i][j] = pix[i, j]

    for row in range(M - 1):
        for col in range(M - 1):
            Em[row + 1][col + 1] = (row * col) / 1
            Gm[row + 1][col + 1] = pow(Gm[row + 1][col + 1], Em[row + 1][col + 1])
    for row in range(N - 1):
        for col in range(N - 1):
            En[row + 1][col + 1] = (row * col) / 1
            Gn[row + 1][col + 1] = pow(Gn[row + 1][col + 1], En[row + 1][col + 1])
    F = np.dot(Gm, f)
    F = np.dot(F, Gn)
    realF = (F).real
    mx = np.max(realF)
    mn = np.min(realF)
    for i in range(M):
        for j in range(N):
            newReal = ((realF[i][j] - mx) / (mx - mn)) * 255
            draw.point((i, j), round(abs(newReal)))
    im = Pref(im)
    im.show()
    return im

image = Image.open("123123.jpg")
image = image.convert('L')
getHits(back_fourier_transform(direct_fourier_transform()))
#getHits(image)
