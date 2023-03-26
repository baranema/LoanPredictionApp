# Import the necessary functions from the corresponding Python files
import streamlit as st
from step1 import acc_pred
from step2 import grade_pred
from step3 import subgrade_pred
from step4 import int_rate_pred


# Define a function to display the main page of the app
def main_page():
    # Display a header for the main page
    st.markdown("# Lending Club Loans App 🎈")
    # Display a header for the sidebar
    st.sidebar.markdown("### Lending Club Loans App 🎈")


# Define a function to display the first step of the app
def step1():
    # Call the `acc_pred()` function to display the loan acceptance prediction
    acc_pred()
    # Display a header for the sidebar
    st.sidebar.markdown("### Loan Acceptance Prediction")


# Define a function to display the second step of the app
def step2():
    # Call the `grade_pred()` function to display the loan grade prediction
    grade_pred()
    # Display a header for the sidebar
    st.sidebar.markdown("### Loan Grade Prediction")


# Define a function to display the third step of the app
def step3():
    # Call the `subgrade_pred()` function to display the loan subgrade prediction
    subgrade_pred()
    # Display a header for the sidebar
    st.sidebar.markdown("### Loan Subgrade Prediction")


# Define a function to display the fourth step of the app
def step4():
    # Call the `int_rate_pred()` function to display the loan interest rate prediction
    int_rate_pred()
    # Display a header for the sidebar
    st.sidebar.markdown("### Loan Interest Rate Prediction")


# Create a dictionary that maps page names to their respective functions
page_names_to_funcs = {
    "Home": main_page,
    "Loan Acceptance": step1,
    "Loan Grade": step2,
    "Loan Subgrade": step3,
    "Loan Interest Rate": step4,
}

# Use the `selectbox()` function from `streamlit` to create a dropdown menu in the sidebar
# that allows the user to select a page
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())

# Call the function associated with the selected page
page_names_to_funcs[selected_page]()
