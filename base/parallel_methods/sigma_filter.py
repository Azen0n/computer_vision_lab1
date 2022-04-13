import numpy as np
from numba import njit, prange


@njit(parallel=True, fastmath=True)
def p_sigma_filter(pixels: np.ndarray, sigma: float, kernel_size: int) -> np.ndarray:
    kernel_radius = int(kernel_size / 2)
    new_pixels = np.zeros((pixels.shape[0], pixels.shape[1]))
    for j in prange(pixels.shape[1] - kernel_size + 1):
        for i in prange(pixels.shape[0] - kernel_size + 1):
            kernel_pixels = pixels[i:i + kernel_size, j:j + kernel_size]
            center = kernel_pixels[kernel_radius, kernel_radius]
            valid_pixels = []
            for pixel in kernel_pixels.flatten():
                if center - sigma <= pixel <= center + sigma:
                    valid_pixels.append(pixel)
            mean = sum(valid_pixels) / len(valid_pixels)
            new_pixels[i + kernel_radius, j + kernel_radius] = int(mean)
    return new_pixels
