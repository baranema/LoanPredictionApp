# Import the necessary packages
import requests
import streamlit as st
import pandas as pd

# API endpoint URL
API_URL = "https://eb-loan-prediction-backend.herokuapp.com/step4_int_rate_prediction/"


# Define function for interest rate prediction
def int_rate_pred():
    # Set title and description
    st.title("Loan Subrade Prediction")
    st.write("Upload your csv file to check anticipatory subgrade of your loan:")

    # Select input type
    st.selectbox("Input Type", ["CSV Upload"])

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file")

    # Read the uploaded file and convert to dictionary
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        loan_info = df.to_dict(orient="records")
    else:
        loan_info = []

    # Define function to get prediction from API
    def get_prediction(payload):
        response = requests.post(API_URL, json=payload)
        return response.status_code, response.json()

    # Run prediction on button click
    if st.button("Predict"):
        # If file uploaded, get predictions and display in dataframe
        if uploaded_file is not None:
            status, predictions = get_prediction(loan_info)
            df = pd.DataFrame(loan_info)
            df.insert(0, "int_rate", "")
            df["int_rate"] = "Unknown"

            # If successful prediction, add predictions to dataframe
            if status == 200:
                for index, prediction in predictions.items():
                    new_index = int(index)
                    if prediction is not None:
                        df.at[new_index, "int_rate"] = prediction

                df = df.sort_values(by="int_rate", ascending=True)
                st.dataframe(df)

            # If unsuccessful prediction, display error message
            else:
                st.write(
                    f"Sorry, there was an error making the prediction. Please try again later. Error message - {predictions}"
                )
