import streamlit as st
from step1 import acc_pred

def main_page():
    st.markdown("# Lending Club Loans App 🎈")
    st.sidebar.markdown("### Lending Club Loans App 🎈")

def page1():
    acc_pred()
    st.sidebar.markdown("### Loan Acceptance Prediction")

page_names_to_funcs = {
    "Home": main_page,
    "Loan Acceptance": page1
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()