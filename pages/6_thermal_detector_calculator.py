import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from TDfiles.func import *
from math import *

st.title('Thermal detector calculator')
# constants
t = 0.1  # start time
step = 0.1  # step size
bp = 0

# session state
if 'alpha_value' not in st.session_state:
    st.session_state.alpha_value = 0.0
if 'alpha_disabled_state' not in st.session_state:
    st.session_state.alpha_disabled_state = True
if 'alpha_dd' not in st.session_state:
    st.session_state.alpha_dd = 'Custom'
if 'graphlist' not in st.session_state:
    st.session_state.graphlist = []
if 'button_press' not in st.session_state:
    st.session_state.button_press = 0
if 'therm_calculate_bool' not in st.session_state:
    st.session_state.therm_calculate_bool = False
if 'therm_test_bool' not in st.session_state:
    st.session_state.therm_test_bool = False

# fucntions
def input_change_callback():
    st.session_state.therm_calculate_bool = False
    st.session_state.therm_test_bool = False


def calc_btn_callback():
    st.session_state.therm_calculate_bool = True



def dd_change_callback():
    st.session_state.therm_calculate_bool = False


def test_btn_callback():
    st.session_state.therm_calculate_bool = False
    st.session_state.therm_test_bool = True

col1, col2, col3 = st.columns(3)
with col1:
    r_input = st.number_input('Input r: (m)', on_change=input_change_callback)
    h_input = st.number_input('Input h: (m)', on_change=input_change_callback)
    alpha_dd = st.selectbox('Select alpha', ('Custom', 'Slow', 'Medium', 'Fast', 'Ultra fast'),
                            on_change=dd_change_callback)

    if alpha_dd == 'Slow':
        st.session_state.alpha_disabled_state = True
        st.session_state.alpha_value = round(1055 / (600 ** 2), 4)
    elif alpha_dd == 'Medium':
        st.session_state.alpha_disabled_state = True
        st.session_state.alpha_value = round(1055 / (300 ** 2), 4)
    elif alpha_dd == 'Fast':
        st.session_state.alpha_disabled_state = True
        st.session_state.alpha_value = round(1055 / (150 ** 2), 4)
    elif alpha_dd == 'Ultra fast':
        st.session_state.alpha_disabled_state = True
        st.session_state.alpha_value = round(1055 / (75 ** 2), 4)
    else:
        a_input = st.number_input('Input a:', value=st.session_state.alpha_value, label_visibility="collapsed",
                                  format="%.5f", on_change=input_change_callback)
        st.session_state.alpha_value = a_input
    st.write('Alpha:', st.session_state.alpha_value)
    a_input = st.session_state.alpha_value
with col2:
    C_input = st.number_input('Input C:', on_change=input_change_callback)
    RTI_input = st.number_input('Input RTI:', on_change=input_change_callback)

with col3:
    Tact_input = st.number_input('Input Tact:', on_change=input_change_callback)
    Tinf_input = st.number_input('Input Tinf:', on_change=input_change_callback)
    calculate_button = st.button('Calculate', on_click=calc_btn_callback)
    test_button = st.button('Test', help='Test calculator with r:2.5, h:2.5, C:0.8, RTI:50, Tact:68, Tinf:20', on_click=test_btn_callback)

if st.session_state.therm_test_bool:
    r_input = 2.5
    h_input = 2.5
    C_input = 0.8
    RTI_input = 50
    Tact_input = 68
    Tinf_input = 20

st.write('r:', r_input, 'h:', h_input, 'alpha:', a_input, 'C:', C_input, 'RTI:', RTI_input, 'Tact:', Tact_input, 'Tinf:', Tinf_input)
st.divider()

st.session_state.therm_calculate_bool
if st.session_state.therm_calculate_bool:
    st.session_state.button_press += 1
    time_result, q_result, result_arr = loop(r_input, h_input, a_input, C_input, RTI_input, Tact_input, Tinf_input,
                                             Tinf_input, t, Tinf_input, step)

    # plotting
    Qypoints = np.array(result_arr[:, 0])
    xpoints = np.array(result_arr[:, 5])
    st.session_state.graphlist.append(xpoints)
    st.session_state.graphlist.append(Qypoints)

    fig = go.Figure()
    for i in range(0, len(st.session_state.graphlist), 2):
        x = st.session_state.graphlist[i]
        y = st.session_state.graphlist[i + 1]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Line {i // 2 + 1}'))
        # fig = px.line(x=st.session_state.graphlist[xpoint], y=st.session_state.graphlist[ypoint], labels={'x':'time (s)', 'y':'Q (MW)'})
        # fig.add_hline(y=graphlist[ypoint][-1])
        # fig.add_shape(type='line', x0=st.session_state.graphlist[xpoint][-1], y0=st.session_state.graphlist[ypoint][-1], x1=900, y1=st.session_state.graphlist[ypoint][-1], xref='x', yref='y')

    st.plotly_chart(fig, use_container_width=True)

    st.session_state.graphlist
    st.session_state.button_press
    result_arr
