import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit as st

def drag_coefficient_model(Re, a1, a2, a3):
    return a1 + (a2 / Re) + (a3 / Re**3)

def fit_drag_coefficient(data, curve_color, points_color):
    # Extract C_d and Re from the data
    Cd_data = data['C_d']
    Re_data = data['Re']

    # Perform curve fitting
    initial_guess = [1.0, 1.0, 1.0]  # Initial guess for the parameters [a1, a2, a3]
    popt, _ = curve_fit(drag_coefficient_model, Re_data, Cd_data, p0=initial_guess)

    # Extract the fitted parameters
    a1_fit, a2_fit, a3_fit = popt

    # Plot the original data and the fitted curve
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(Re_data, Cd_data, label='Data', color=points_color, s=50, linewidth=5.0, edgecolor='black')
    ax.plot(Re_data, drag_coefficient_model(Re_data, a1_fit, a2_fit, a3_fit), color=curve_color, label='Fitted Curve', linewidth=5.0)
    ax.set_xlabel('Reynolds number (Re)', fontsize=20)
    ax.set_ylabel('Drag Coefficient ($C_d$)', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20, size=6, width=2.5)
    ax.legend(fontsize=20)

    st.pyplot(fig)

    return a1_fit, a2_fit, a3_fit

def main():
    st.title('Drag Coefficient Fitting')

    uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.subheader('Data from CSV file:')
        st.write(data)

        # Get all possible color names
        color_names = [name for name in mcolors.CSS4_COLORS]
        
        # Set default colors
        default_curve_color = 'red'
        default_points_color = 'black'

        curve_color = st.selectbox('Select curve color:', color_names, index=color_names.index(default_curve_color))
        points_color = st.selectbox('Select points color:', color_names,  index=color_names.index(default_points_color))

        fitted_a1, fitted_a2, fitted_a3 = fit_drag_coefficient(data, curve_color, points_color)

        st.subheader('Fitted Coefficients:')
        st.write(f"a1 = {fitted_a1}, a2 = {fitted_a2}, a3 = {fitted_a3}")

if __name__ == '__main__':
    main()

