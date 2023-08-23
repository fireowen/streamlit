import streamlit as st

st.title('Radsolver')
# define the value for the constant sigma in the equation
sigma = 5.67e-8


# define a function to solve the equation
def solve_equation(F, e, T):
    return F * e * sigma * T ** 4 / 1000


# set up page
col1, col2, col3 = st.columns(3)

# create inputs
with col1:
    F_input = st.number_input('Input F')

with col2:
    e_input = st.number_input('Input e')

with col3:
    T_input = st.number_input('Input T')

# create the solve button
solve_button = st.button('Solve')
st.divider()
if solve_button:
    result = solve_equation(F_input, e_input, T_input)
    st.write(f"Radiation is {result:.2f} kW/m\u00B2")
