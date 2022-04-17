import numpy as np
from numba import njit, prange


@njit(parallel=True, fastmath=True)
def p_gaussian_filter(pixels: np.ndarray, sigma: float) -> np.ndarray:
    kernel_radius = int(np.ceil(3 * sigma) - 1)
    kernel_size = int(kernel_radius * 2 + 1)

    filter_ = np.zeros((kernel_size, kernel_size))
    for i in prange(kernel_size):
        for j in prange(kernel_size):
            filter_[i][j] = np.exp(-((i - kernel_radius) ** 2 + (j - kernel_radius) ** 2) / (2 * sigma * sigma))
    filter_ = filter_ / np.sum(filter_)

    new_pixels = np.zeros((pixels.shape[0], pixels.shape[1]))
    for j in prange(pixels.shape[1] - kernel_size + 1):
        for i in prange(pixels.shape[0] - kernel_size + 1):
            kernel_pixels = pixels[i:i + kernel_size, j:j + kernel_size]
            new_pixels[i + kernel_radius, j + kernel_radius] = int(np.sum(filter_ * kernel_pixels))
    return new_pixels
