import streamlit as st
import numpy as np
import math

st.title('Line source radiation model')

# sessions states
if 'line_source_calc_bool' not in st.session_state:
    st.session_state.line_source_calc_bool = False


# functions
def input_btn_callback():
    st.session_state.line_source_calc_bool = False


def calc_btn_callback():
    st.session_state.line_source_calc_bool = True


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


col1, col2, col3 = st.columns(3)

with col1:
    xrad_input = st.number_input('X_rad:', on_change=input_btn_callback, value=0.35)
    r_fs_input = st.number_input('Radius of fuel source:', on_change=input_btn_callback)
    h_fs_input = st.number_input('Height of fuel source:', on_change=input_btn_callback)
    alpha_input = st.number_input('Alpha:', on_change=input_btn_callback, value=0.04667, disabled=True)
with col2:
    hrr_input = st.number_input('HRR (kW):', on_change=input_btn_callback, disabled=False)
    i_input = st.number_input('Discretization points:', on_change=input_btn_callback, min_value=1)
    tau_input = st.number_input('Amb transmisibity:', on_change=input_btn_callback)
    time_input = st.number_input('Length of simulation (s):', on_change=input_btn_callback, min_value=1, disabled=True)
with col3:
    dt_input = st.number_input('Dt:', on_change=input_btn_callback)
    lt_input = st.number_input('Lt:', on_change=input_btn_callback)
    ht_input = st.number_input('Ht:', on_change=input_btn_callback)

calc_button = st.button('Calculate', on_click=calc_btn_callback)

if st.session_state.line_source_calc_bool:
    q = alpha_input * 1 ** 2
    qr_pool, qr_crib = line_source_calculate(xrad_input, r_fs_input, h_fs_input, hrr_input, i_input, tau_input,
                                             dt_input, lt_input, ht_input)
    arr2 = np.array([1, q, qr_pool, qr_crib])
    # for j in range(2, time_input):
    #     q = alpha_input * j ** 2
    #     qr_pool, qr_crib = line_source_calculate(xrad_input, r_fs_input, h_fs_input, q, i_input, tau_input, dt_input,
    #                                              lt_input, ht_input)
    #
    #     temparr = np.array([j, q, qr_pool, qr_crib])
    #     arr2 = np.vstack((arr2, temparr))
    st.write('qr pool:', qr_pool, 'qr crib:', qr_crib)
    #arr2
    # sqrt = math.sqrt(dt_input ** 2 + lt_input ** 2)
    # xrad_multi = (xrad_input * tau_input * hrr_input) / (8 * math.pi * (i_input - 1))
    # hf = 0.235 * hrr_input ** (2 / 5) + 1.02 * 2 * r_fs_input
    #
    # sqrt, xrad_multi, hf
    #
    # hi = 0
    # wi = 1.55 / (1 + ((hi / hf) / 0.625) ** (20 / 3))
    # ri_pool = -3 * (hi / hf) ** 3 + 5.5 * (hi / hf) ** 2 - 3.5 * (hi / hf) + 1
    # ri_crib = -2 * (hi / hf) ** 3 + 3.5 * (hi / hf) ** 2 - 2.5 * (hi / hf) + 1
    # Ri_pool = (wi * sqrt - ri_pool * r_fs_input) / (
    #         ((sqrt - ri_pool * r_fs_input) ** (2) + (ht_input - h_fs_input - hi) ** (2)) ** (3 / 2))
    # Ri_crib = (wi * sqrt - ri_crib * r_fs_input) / (
    #         ((sqrt - ri_crib * r_fs_input) ** (2) + (ht_input - h_fs_input - hi) ** (2)) ** (3 / 2))
    # arr1 = np.array([hi, wi, ri_pool, ri_crib, Ri_pool, Ri_crib])
    #
    # for i in range(2, i_input + 1):
    #     hi = ((i - 1) / (i_input - 1)) * hf
    #     wi = 1.55 / (1 + ((hi / hf) / 0.625) ** (20 / 3))
    #     ri_pool = -3 * (hi / hf) ** 3 + 5.5 * (hi / hf) ** 2 - 3.5 * (hi / hf) + 1
    #     ri_crib = -2 * (hi / hf) ** 3 + 3.5 * (hi / hf) ** 2 - 2.5 * (hi / hf) + 1
    #     Ri_pool = (wi * sqrt - ri_pool * r_fs_input) / (
    #             ((sqrt - ri_pool * r_fs_input) ** (2) + (ht_input - h_fs_input - hi) ** (2)) ** (3 / 2))
    #     Ri_crib = (wi * sqrt - ri_crib * r_fs_input) / (
    #             ((sqrt - ri_crib * r_fs_input) ** 2 + (ht_input - h_fs_input - hi) ** (2)) ** (3 / 2))
    #
    #     arrtemp = np.array([hi, wi, ri_pool, ri_crib, Ri_pool, Ri_crib])
    #     arr1 = np.vstack((arr1, arrtemp))
    #
    # arr1
    # Ri_poolarr = arr1[:, -2]
    # qr_pool = np.sum(Ri_poolarr[:-1] + Ri_poolarr[1:]) * xrad_multi
    #
    # Ri_cribarr = arr1[:, -1]
    # qr_crib = np.sum(Ri_cribarr[:-1] + Ri_cribarr[1:]) * xrad_multi
    #
    # st.write('qr pool:', qr_pool, 'qr crib:', qr_crib)
