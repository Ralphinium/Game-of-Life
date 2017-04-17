from numpy import array, fft
from scipy import fftpack
import numpy as np


def fft_convolve(x: np.ndarray, y: np.ndarray, wrap_around=False):
    """
    Returns the convolution of two given matrices, `x` and `y`. 
    
    A convolution is an operation between two matrices. Each element of the first matrix is added to its neighbors,
    weighted by the second matrix. As such, the result of the convolution will always be the same size as the first
    matrix. The second matrix need not be the same size as the first matrix. The second matrix is sometimes called the 
    "convolution matrix" or in image processing, the "kernel" or "mask".
    
    Due to the Convolution theorem, the convolution between two matrices can be computed efficiently using FFTs.
    Denoting matrix convolution by <*> and matrix multiplication by *, we have (roughly):
        x<*>y = ifft(fft(x)*(fft(y))
    
    Given two matrices `x` and `y`, suppose `x` is an M-by-N matrix and `y` is a P-by-Q matrix. First, we will zero-pad
    both matrices so they are the same shape. We then compute the convolution using the formula above, cutting the 
    resulting matrices to the size of the `x` and removing imaginary parts due to round-off errors. 
    
    :param x: The first matrix which will determine the size of the result. 
    :param y: The kernel or mask.
    :param wrap_around: Boundary conditions. If `True`, we do circular convolution. Else, we pad the matrices with 
        enough zeros to avoid wrapping around.
    :return: The result of the convolution, a 2D matrix with the same dimensions as `x`.
    """

    s1 = array(x.shape)
    s2 = array(y.shape)
    if not wrap_around:
        shape = s1 + s2 - 1
        optimal_shape = [fftpack.helper.next_fast_len(int(d)) for d in shape]
    else:
        shape = s1
        optimal_shape = s1
    slices = tuple([slice(0, int(s)) for s in shape])

    fft_x = fft.fft2(x, optimal_shape)
    fft_y = fft.fft2(y, optimal_shape)
    ret = fft.ifft2(fft_x * fft_y, optimal_shape)[slices].copy()

    if wrap_around:
        m, n = x.shape
        ret = np.roll(ret, -int(m/2) + 1, axis=0)
        ret = np.roll(ret, -int(n/2) + 1, axis=1)
        return ret
    else:
        start_ind = (optimal_shape - s1) // 2
        end_ind = start_ind + s1
        slices = tuple([slice(start_ind[k], end_ind[k]) for k in range(len(end_ind))])
        return ret[slices]


def int_fft_convolve(x: np.ndarray, y: np.ndarray, wrap_around=False):
    """
    Returns the convolution of `x` and `y`, using the above algorithm. 
    
    Also only takes the real part of the matrix, and rounds them all, to compensate for the possible rounding errors in
    the algorithm.
    :param x: The first matrix which will determine the size of the result. 
    :param y: The kernel or mask.
    :param wrap_around: Boundary conditions. If `True`, we do circular convolution. Else, we pad the matrices with 
        enough zeros to avoid wrapping around.
    :return: The result of the convolution, a 2D matrix with the same dimensions as `x`.
    """
    return np.real(fft_convolve(x, y, wrap_around)).round()