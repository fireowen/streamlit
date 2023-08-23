import streamlit as st
import math
import pandas as pd


# functions
def off_calc(fire_area, fuel_load, ext_eff):
    t_ext = 3.3 * math.sqrt(fire_area)

    if ext_eff == 0:
        fire_flow = 0
    else:
        fire_flow = (0.058275058275 * fuel_load * math.sqrt(fire_area) / ext_eff)

    return t_ext, fire_flow


def def_calc(fire_area, fuel_load, ext_eff, view_f):
    def_t_ext = 3.3 * math.sqrt(fire_area)

    if ext_eff == 0:
        def_fire_flow = 0
    else:
        def_fire_flow = (view_f / ext_eff) * (0.005 * fuel_load * math.sqrt(fire_area))

    return def_t_ext, def_fire_flow


def calc_btn_callback():
    st.session_state.button_press += 1
    st.session_state.calculate_bool = True
    st.session_state.undo_bool = False


def undo_btn_callback():
    st.session_state.button_press -= 1
    st.session_state.calculate_bool = False
    st.session_state.undo_bool = True


def num_input_callback():
    st.session_state.calculate_bool = False
    st.session_state.undo_bool = False


# initialise session state
if 'fire_area' not in st.session_state:
    st.session_state.fire_area = 0.0
if 'fuel_load' not in st.session_state:
    st.session_state.fuel_load = 0.0
if 'ext_eff' not in st.session_state:
    st.session_state.ext_eff = 0.0
if 'exposures' not in st.session_state:
    st.session_state.exposures = 0
if 'viewF' not in st.session_state:
    st.session_state.viewF = 0.0
if 'button_press' not in st.session_state:
    st.session_state.button_press = 0
if "mdf" not in st.session_state:
    st.session_state.mdf = pd.DataFrame(
        columns=['Time to extinguish (min)', 'Off Fire flow (L/s)', 'Def Fire flow (L/s)', 'Off + def Volume (L)', '0.5E Volume (L)'])
if "calculate_bool" not in st.session_state:
    st.session_state.calculate_bool = False
if "undo_bool" not in st.session_state:
    st.session_state.undo_bool = False

st.title("Fire fighting calculators")

st.header("Offensive and defensive firefighting flows")

with st.expander("Inputs:", expanded=True):
    col1, col2, col3, = st.columns(3)
    with col1:
        st.session_state.fire_area = st.number_input("Fire area (m\u00b2)", value=st.session_state.fire_area, on_change=num_input_callback)
        st.session_state.exposures = st.number_input("Number of exposures", value=st.session_state.exposures, on_change=num_input_callback)
    with col2:
        st.session_state.fuel_load = st.number_input("Fuel load (MJ/m\u00b2)", value=st.session_state.fuel_load, on_change=num_input_callback)
        st.session_state.viewF = st.number_input("View factor", value=st.session_state.viewF, on_change=num_input_callback)
    with col3:
        st.session_state.ext_eff = st.number_input("Extinguishing efficiency", value=st.session_state.ext_eff, on_change=num_input_callback)

col4, col5, col6 = st.columns([1, 1, 3])
with col4:
    calculate_btn = st.button('Calculate', on_click=calc_btn_callback)
with col5:
    undo_btn = st.button('Undo', on_click=undo_btn_callback)


if st.session_state.calculate_bool:

    t_ext, off_fire_flow = off_calc(st.session_state.fire_area,
                                st.session_state.fuel_load,
                                st.session_state.ext_eff)
    t_ext, def_fire_flow = def_calc(st.session_state.fire_area,
                                st.session_state.fuel_load,
                                st.session_state.ext_eff,
                                st.session_state.viewF)
    new_row = pd.DataFrame({
        'Time to extinguish (min)': [f"{round(t_ext, 2)}"],
        'Off Fire flow (L/s)': [f"{round(off_fire_flow / 60, 2):,}"],
        'Def Fire flow (L/s)': [f"{round(def_fire_flow / 60, 2)}"],
        'Off + def Volume (L)': [f"{round(t_ext * (off_fire_flow + (def_fire_flow * st.session_state.exposures)),2):,}"],
        '0.5E Volume (L)': [f"{round(0.5 * st.session_state.fire_area * st.session_state.fuel_load, 2):,}"]
    })
    #t_ext,off_fire_flow,def_fire_flow,st.session_state.exposures
    st.write(f"Off volume: {round((t_ext * off_fire_flow),2):,}. Def volume: {round((t_ext * def_fire_flow * st.session_state.exposures),2):,}.")
    st.session_state.mdf = pd.concat([st.session_state.mdf, new_row])

if st.session_state.undo_bool:
    st.session_state.mdf = st.session_state.mdf[:-1]

st.divider()
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
results_table = st.table(st.session_state.mdf)
