import streamlit as st

# define the value for the constant sigma in the equation
row = 1.2
Ta = 293.15
cp = 1
g = 9.81


# define a function to solve the equation
def solve_equation(Q, row, Ta, cp, g):
    return (Q / (row * Ta * cp * g ** 0.5)) ** (2 / 5)


# create the input fields and a label for each
Q_input = st.number_input("Enter Q:")

# create the solve button
solve_button = st.button("Calculate")
st.divider()
if solve_button:
    result = solve_equation(Q_input, row, Ta, cp, g)
    st.write(f'Fire diameter is: {result:.2f} m')
    st.write(f'Fire diameter / 10 is: {result / 10:.2f}')
    st.write(f'Fire diameter / 5 is: {result / 5:.2f}')
