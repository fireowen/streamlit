import math
from math import *
import numpy as np


def time_hrr_r_hf_calculate(time_end, hrrpua, alpha):
    result_arr = np.empty((time_end, 4))
    for i in range(1, time_end+1):
        q = alpha * i**2
        r = math.sqrt((q / (hrrpua*pi)))
        hf = 0.235 * q ** (2/5) + 1.02 * 2 * r

        result_arr[i-1] = [i, q, r, hf]

    return result_arr


def location_array_calculate():
    array_size = 101
    array = np.zeros((array_size, array_size))

    for i in range(array_size):
        for j in range(array_size):
            value = math.sqrt(((50 - i) / 10) ** 2 + ((j - 50) / 10) ** 2)
            array[i][j] = value

    return array



def line_source_calculate(x_rad, r_fs, h_fs, hrr, i_input, tau, dt, lt, ht):
    sqrt = math.sqrt(dt ** 2 + lt ** 2)
    multiplier = (x_rad * tau * hrr) / (8 * math.pi * (i_input - 1))
    hf = 0.235 * hrr ** (2 / 5) + 1.02 * 2 * r_fs
    # sqrt, multiplier, hf

    hi = 0
    wi = 1.55 / (1 + ((hi / hf) / 0.625) ** (20 / 3))
    ri_pool = -3 * (hi / hf) ** 3 + 5.5 * (hi / hf) ** 2 - 3.5 * (hi / hf) + 1
    ri_crib = -2 * (hi / hf) ** 3 + 3.5 * (hi / hf) ** 2 - 2.5 * (hi / hf) + 1
    Ri_pool = (wi * sqrt - ri_pool * r_fs) / (
            ((sqrt - ri_pool * r_fs) ** (2) + (ht - h_fs - hi) ** (2)) ** (3 / 2))
    Ri_crib = (wi * sqrt - ri_crib * r_fs) / (
            ((sqrt - ri_crib * r_fs) ** (2) + (ht - h_fs - hi) ** (2)) ** (3 / 2))
    arr1 = np.array([hi, wi, ri_pool, ri_crib, Ri_pool, Ri_crib])

    for i in range(2, i_input + 1):
        hi = ((i - 1) / (i_input - 1)) * hf
        wi = 1.55 / (1 + ((hi / hf) / 0.625) ** (20 / 3))
        ri_pool = -3 * (hi / hf) ** 3 + 5.5 * (hi / hf) ** 2 - 3.5 * (hi / hf) + 1
        ri_crib = -2 * (hi / hf) ** 3 + 3.5 * (hi / hf) ** 2 - 2.5 * (hi / hf) + 1
        Ri_pool = (wi * sqrt - ri_pool * r_fs) / (
                ((sqrt - ri_pool * r_fs) ** (2) + (ht - h_fs - hi) ** (2)) ** (3 / 2))
        Ri_crib = (wi * sqrt - ri_crib * r_fs) / (
                ((sqrt - ri_crib * r_fs) ** 2 + (ht - h_fs - hi) ** (2)) ** (3 / 2))

        arrtemp = np.array([hi, wi, ri_pool, ri_crib, Ri_pool, Ri_crib])
        arr1 = np.vstack((arr1, arrtemp))

    # arr1
    Ri_poolarr = arr1[:, -2]
    qr_pool = np.sum(Ri_poolarr[:-1] + Ri_poolarr[1:]) * multiplier

    Ri_cribarr = arr1[:, -1]
    qr_crib = np.sum(Ri_cribarr[:-1] + Ri_cribarr[1:]) * multiplier

    return qr_pool, qr_crib
