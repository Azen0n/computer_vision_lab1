from PIL import Image

from base.lab2.blurring import gaussian_filter, sigma_filter
from base.lab2.lab2_processing import mean_absolute_error, mean_squared_error, unsharp_masking


def gaussian(image: Image):
    print('gaussian_filter')
    for sigma_ in range(1, 11):
        processed_image = gaussian_filter(image, sigma_)
        mae = mean_absolute_error(image, processed_image)
        mse = mean_squared_error(image, processed_image)
        print(f'sigma: {sigma_}\tMAE: {mae:.2f}\tMSE: {mse:.2f}')
    print()


def sigma(image: Image):
    print('sigma_filter')
    for sigma_ in range(20, 71, 10):
        print(f'sigma: {sigma_}')
        for kernel_size in range(3, 8, 2):
            processed_image = sigma_filter(image, sigma_, kernel_size)
            mae = mean_absolute_error(image, processed_image)
            mse = mean_squared_error(image, processed_image)
            print(f'kernel_size: {kernel_size}\tMAE: {mae:.2f}\tMSE: {mse:.2f}')
    print()


def sharpening(image: Image):
    methods = ['square_filter', 'median_filter']
    for method in methods:
        print(f'Method: {method}')
        for kernel_size in [3, 5]:
            print(f'kernel_size = {kernel_size}')
            for lambda_ in range(-10, 11, 5):
                lambda_ /= 10
                processed_image = unsharp_masking(image, lambda_, method, kernel_size)
                mae = mean_absolute_error(image, processed_image)
                mse = mean_squared_error(image, processed_image)
                print(f'lambda: {lambda_}\tMAE: {mae:.2f}\tMSE: {mse:.2f}')
            print()

    print()
    print(f'Method: gaussian_filter')
    for sigma_ in range(2, 5):
        print(f'sigma: {sigma_}')
        for lambda_ in range(-10, 11, 5):
            lambda_ /= 10
            processed_image = unsharp_masking(image, lambda_, 'gaussian_filter', sigma_)
            mae = mean_absolute_error(image, processed_image)
            mse = mean_squared_error(image, processed_image)
            print(f'lambda_: {lambda_}\tMAE: {mae:.2f}\tMSE: {mse:.2f}')
        print()

    print()
    print(f'Method: sigma_filter')
    for sigma_ in [50, 60]:
        print(f'sigma: {sigma_}')
        for kernel_size in [3, 5]:
            print(f'kernel_size: {kernel_size}')
            for lambda_ in range(-10, 11, 5):
                lambda_ /= 10
                processed_image = unsharp_masking(image, lambda_, 'sigma_filter', sigma_, kernel_size)
                mae = mean_absolute_error(image, processed_image)
                mse = mean_squared_error(image, processed_image)
                print(f'lambda_: {lambda_}\tMAE: {mae:.2f}\tMSE: {mse:.2f}')
            print()


def main():
    # noised_image = Image.open('Noised_Prague.png')
    # gaussian(noised_image)
    # sigma(noised_image)

    image = Image.open('../Prague.png')
    sharpening(image)


if __name__ == '__main__':
    main()
