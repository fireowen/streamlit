import streamlit as st
import numpy as np
import math
from linesourceFunc.lineSource import *
import plotly.graph_objs as go

st.title('Line source radiation model')

# sessions states
if 'line_source_calc_bool' not in st.session_state:
    st.session_state.line_source_calc_bool = False


# functions
def input_btn_callback():
    st.session_state.line_source_calc_bool = False


def calc_btn_callback():
    st.session_state.line_source_calc_bool = True


# def line_source_calculate(x_rad, r_fs, h_fs, hrr, i_input, tau, dt, lt, ht):
#     sqrt = math.sqrt(dt ** 2 + lt ** 2)
#     multiplier = (x_rad * tau * hrr) / (8 * math.pi * (i_input - 1))
#     hf = 0.235 * hrr ** (2 / 5) + 1.02 * 2 * r_fs
#     # sqrt, multiplier, hf
#
#     hi = 0
#     wi = 1.55 / (1 + ((hi / hf) / 0.625) ** (20 / 3))
#     ri_pool = -3 * (hi / hf) ** 3 + 5.5 * (hi / hf) ** 2 - 3.5 * (hi / hf) + 1
#     ri_crib = -2 * (hi / hf) ** 3 + 3.5 * (hi / hf) ** 2 - 2.5 * (hi / hf) + 1
#     Ri_pool = (wi * sqrt - ri_pool * r_fs) / (
#             ((sqrt - ri_pool * r_fs) ** (2) + (ht - h_fs - hi) ** (2)) ** (3 / 2))
#     Ri_crib = (wi * sqrt - ri_crib * r_fs) / (
#             ((sqrt - ri_crib * r_fs) ** (2) + (ht - h_fs - hi) ** (2)) ** (3 / 2))
#     arr1 = np.array([hi, wi, ri_pool, ri_crib, Ri_pool, Ri_crib])
#
#     for i in range(2, i_input + 1):
#         hi = ((i - 1) / (i_input - 1)) * hf
#         wi = 1.55 / (1 + ((hi / hf) / 0.625) ** (20 / 3))
#         ri_pool = -3 * (hi / hf) ** 3 + 5.5 * (hi / hf) ** 2 - 3.5 * (hi / hf) + 1
#         ri_crib = -2 * (hi / hf) ** 3 + 3.5 * (hi / hf) ** 2 - 2.5 * (hi / hf) + 1
#         Ri_pool = (wi * sqrt - ri_pool * r_fs) / (
#                 ((sqrt - ri_pool * r_fs) ** (2) + (ht - h_fs - hi) ** (2)) ** (3 / 2))
#         Ri_crib = (wi * sqrt - ri_crib * r_fs) / (
#                 ((sqrt - ri_crib * r_fs) ** 2 + (ht - h_fs - hi) ** (2)) ** (3 / 2))
#
#         arrtemp = np.array([hi, wi, ri_pool, ri_crib, Ri_pool, Ri_crib])
#         arr1 = np.vstack((arr1, arrtemp))
#
#     # arr1
#     Ri_poolarr = arr1[:, -2]
#     qr_pool = np.sum(Ri_poolarr[:-1] + Ri_poolarr[1:]) * multiplier
#
#     Ri_cribarr = arr1[:, -1]
#     qr_crib = np.sum(Ri_cribarr[:-1] + Ri_cribarr[1:]) * multiplier
#
#     return qr_pool, qr_crib


col1, col2, col3 = st.columns(3)

with col1:
    xrad_input = st.number_input('X_rad:', on_change=input_btn_callback, value=0.35)
    r_fs_input = st.number_input('Radius of fuel source:', on_change=input_btn_callback, disabled=True)
    h_fs_input = st.number_input('Height of fuel source:', on_change=input_btn_callback)
    alpha_input = st.number_input('Alpha:', on_change=input_btn_callback, disabled=False, value=0.04667)
with col2:
    hrr_input = st.number_input('HRRPUA (kW):', on_change=input_btn_callback, disabled=False, value=500)
    i_input = st.number_input('Discretization points:', on_change=input_btn_callback, min_value=1, disabled=True)
    tau_input = st.number_input('Amb transmisibity:', on_change=input_btn_callback, value=1.0)
    time_input = st.number_input('Length of simulation (s):', on_change=input_btn_callback, min_value=1, value=50)
with col3:
    dt_input = st.number_input('Dt:', on_change=input_btn_callback, disabled=True)
    lt_input = st.number_input('Lt:', on_change=input_btn_callback, disabled=True)
    ht_input = st.number_input('Ht:', on_change=input_btn_callback, value=1.5)

calc_button = st.button('Calculate', on_click=calc_btn_callback)

if st.session_state.line_source_calc_bool:
    i_input = 11  # hard code discretization
    t_hrr_r_hf_array = time_hrr_r_hf_calculate(time_input, hrr_input, alpha_input)
    pos_array = location_array_calculate()
    frames = np.empty((time_input, 101, 101))
    for i in range(1, time_input):
        for j in range(101):
            for k in range(101):
                #x = (k - 50) / 10
                #y = (50 - j) / 10
                q = t_hrr_r_hf_array[i, 1]
                r_fs = t_hrr_r_hf_array[i, 2]
                #h_fs = t_hrr_r_hf_array[i, 3]

                dt = pos_array[j][k]

                qr_pool, qr_crib = line_source_calculate(xrad_input, r_fs, h_fs_input, q, i_input, tau_input, dt,
                                                         lt_input,
                                                         ht_input)
                frames[i, j, k] = qr_crib

    t_hrr_r_hf_array
    #frames

    # frames
    fig = go.Figure(
        data=[go.Heatmap(z=frames[0],zmin=0,zmax=4, x=[0,0.05], y=[0,0.05])],
        layout=go.Layout(
            title="Frame 0",
            title_x=0.5,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None]),
                         dict(label="Pause",
                              method="animate",
                              args=[None,
                                    {"frame": {"duration": 0, "redraw": False},
                                     "mode": "immediate",
                                     "transition": {"duration": 0}}],
                              )])]

        ),
        frames=[go.Frame(data=[go.Heatmap(z=frames[i])],
                         layout=go.Layout(title_text=f"Frame {i}"))
                for i in range(1, time_input)]
    )
    steps = []
    for i in range(len(fig.data)):
        step = {
            "method": "update",
            "args": [
                {"visible": [False] * len(fig.data)},
                {"title": "Sliders switched to step: " + str(i)}  # layout attribute
            ]
        }
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)
    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps
    )]
    fig.update_layout(sliders=sliders)
    #fig.update_xaxes(range=[-5, 5])
    #fig.update_yaxes(range=[-5, 5])
    #fig.show()
    st.plotly_chart(fig, use_container_width=True, theme=None)
    # hf = 0.235 * hrr_input ** (2 / 5) + 1.02 * 2 * r_fs_input
    # qr_pool, qr_crib = line_source_calculate(xrad_input, r_fs_input, h_fs_input, hrr_input, i_input, tau_input,
    #                                          dt_input, lt_input, 0)
    # arr2 = np.array([0, hrr_input, qr_pool, qr_crib])
    # for j in range(1, round(hf * 100)):
    #     # q = alpha_input * j ** 2
    #     qr_pool, qr_crib = line_source_calculate(xrad_input, r_fs_input, h_fs_input, hrr_input, i_input, tau_input,
    #                                              dt_input,
    #                                              lt_input, j / 100)
    #
    #     temparr = np.array([j / 100, hrr_input, qr_pool, qr_crib])
    #     arr2 = np.vstack((arr2, temparr))
    # st.write('qr pool:', qr_pool, 'qr crib:', qr_crib)
    # arr2
