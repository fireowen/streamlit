from math import *
import numpy as np

def deltaTmax(r, H, Q):
    ratio = r / H

    if ratio < 0.18:
        result = ((16.9 * Q ** (2 / 3)) / (H ** (5 / 3)))
    else:
        result = ((5.38 * ((Q / r) ** (2 / 3))) / (H))

    return result


def Umax(r, H, Q):
    ratio = r / H

    if ratio < 0.15:
        result1 = 0.96 * (Q / H) ** (1 / 3)
    else:
        result1 = (0.195 * Q ** (1 / 3) * H ** (1 / 2)) / (r ** (5 / 6))

    return result1

def deltaTe(u,RTI,Tg,C,Te,Ta,step):
    result2 = ((sqrt(u) / RTI) * (Tg - (1 + (C / (sqrt(u)))) * Te - Ta)) * step

    return result2

def loop(r, H, a, C, RTI, T_act, T_i, T_a, t, Te, step):
    Q = a * t ** 2
    Tg = deltaTmax(r, H, Q)
    u = Umax(r, H, Q)

    dTe = ((sqrt(u) / RTI) * (Tg - (1 + (C / (sqrt(u)))) * (T_i - T_a))) * step
    Te = Te + dTe
    arr1 = np.array([Q, Tg, u, dTe, Te, t])
    t = t + step

    while Te < T_act:
        Q = a * t ** 2
        Tg = deltaTmax(r, H, Q)
        u = Umax(r, H, Q)

        dTe = ((sqrt(u) / RTI) * (Tg - (1 + (C / (sqrt(u)))) * (Te - T_a))) * step
        Te = Te + dTe
        arrTemp = np.array([(Q/1000), Tg, u, dTe, Te, t])
        arr1 = np.vstack((arr1, arrTemp))
        t = t + step

    return t, Q, arr1