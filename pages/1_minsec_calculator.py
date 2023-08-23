import streamlit as st


st.set_page_config(
    page_title="min\:sec converter"
)
st.title("min\:sec converter")

timetype = ["seconds", "min:sec", "minutes (decimal)"]

input_type = st.selectbox('What is the input type?', timetype)
number = st.text_input('Input number')

try:
    if input_type == "minutes (decimal)":
        mins, secs = map(int, number.split('.'))
    elif input_type == "seconds":
        number = int(number)
    elif input_type == "min:sec":
        mins, secs = map(int, number.split(':'))

    output_type = st.selectbox('What is the output type?', timetype)

    # Perform different actions based on the combination of input_type and output_type
    if input_type == "minutes (decimal)" and output_type == "minutes (decimal)":
        # Perform action for input_type = "minutes (decimal)" and output_type = "minutes (decimal)"
        outnum = 'No conversion needed'

    elif input_type == "minutes (decimal)" and output_type == "seconds":
        # Perform action for input_type = "minutes (decimal)" and output_type = "seconds"
        outnum = f'{mins * 60 + secs} {output_type}'

    elif input_type == "minutes (decimal)" and output_type == "min:sec":
        # Perform action for input_type = "minutes (decimal)" and output_type = "min:sec"
        outnum = f'{mins}:{str(secs * 6).zfill(2)} min\:sec'

    elif input_type == "min:sec" and output_type == "minutes (decimal)":
        # Perform action for input_type = "min:sec" and output_type = "minutes (decimal)"
        outnum = f'{mins}.{int(secs / 0.6)} {output_type}'

    elif input_type == "min:sec" and output_type == "seconds":
        # Perform action for input_type = "min:sec" and output_type = "seconds"
        outnum = f'{mins * 60 + secs} {output_type}'

    elif input_type == "min:sec" and output_type == "min:sec":
        # Perform action for input_type = "min:sec" and output_type = "min:sec"
        outnum = 'No conversion needed'

    elif input_type == "seconds" and output_type == "minutes (decimal)":
        # Perform action for input_type = "min:sec" and output_type = "minutes (decimal)"
        outnum = f'{round(number / 60, 2)} {output_type}'

    elif input_type == "seconds" and output_type == "seconds":
        # Perform action for input_type = "min:sec" and output_type = "seconds"
        outnum = 'No conversion needed'

    elif input_type == "seconds" and output_type == "min:sec":
        # Perform action for input_type = "min:sec" and output_type = "min:sec"
        output_type = "min\:sec"
        outnum = f'{number // 60}:{str(number % 60).zfill(2)} {output_type}'

except ValueError:
    outnum = 'Invalid input'

st.write(outnum)