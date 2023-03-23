import streamlit as st
import step1

def main_page():
    st.markdown("# Loan Prediction App 🎈")
    st.sidebar.markdown("# Loan Prediction App 🎈")

def page1():
    step1.app()

page_names_to_funcs = {
    "Home": main_page,
    "Loan Acceptance": page1
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()