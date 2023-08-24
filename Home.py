import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_keyup import st_keyup
from streamlit_extras.switch_page_button import switch_page

import plotly

#add_logo(r'images\logo.jpg', height=120)

st.title('Safyre calculator homepage')

st.markdown(
    """
    Select a claculator from the ** sidebar **
    
    Brought to you by fire_owen
    
    """
)

#define search tags !!! make sure page name is the same as the tag key !!!
tags = {
    "minsec calculator": ["minutes", "seconds", "time", "minsec", "min:sec"],
    "equiv fire sev surface": ["equivalent", "fire", "severity"],
    "fire fighting flows calculator": ["fire", "fighting", "flow", "offensive", "defensive"],
    "radsolver": ["radiation", "rad", "solver", "solve"],
    "characteristic fire diameter calculator": ["fire", "characteristic", "diameter", "fire diameter", "pyrosim"]
}

searchbar = st_keyup("Search calculators")

if searchbar:
    matching_keys = [key for key, value in tags.items() if any(searchbar.lower() in tag.lower() for tag in value)]
    for key in matching_keys:
        button_label = f"{key}"
        if st.button(button_label):
            switch_page(f'{button_label}')
