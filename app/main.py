import streamlit as st
from step1 import acc_pred
from step2 import grade_pred

def main_page():
    st.markdown("# Lending Club Loans App 🎈")
    st.sidebar.markdown("### Lending Club Loans App 🎈")

def step1():
    acc_pred()
    st.sidebar.markdown("### Loan Acceptance Prediction")

def step2():
    grade_pred()
    st.sidebar.markdown("### Loan Grade Prediction")

page_names_to_funcs = {
    "Home": main_page,
    "Loan Acceptance": step1,
    "Loan Grade": step2
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()