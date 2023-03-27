# Import the necessary packages
import pandas as pd
import requests
import streamlit as st

API_URL = "https://eb-loan-prediction-backend.herokuapp.com/step2_grade_prediction/"


# Define function for loan grade prediction
def grade_pred():
    # Display title and message
    st.title("Loan Grade Prediction")
    st.write("Upload your csv file to check anticipatory grade of your loan:")

    # Display select box for input type and file uploader
    st.selectbox("Input Type", ["CSV Upload"])
    uploaded_file = st.file_uploader("Upload CSV file")

    # Read CSV file and convert to dictionary if file uploaded
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        loan_info = df.to_dict(orient="records")
    else:
        loan_info = []

    # Function to send loan information to API and get predicted grades
    def get_prediction(payload):
        response = requests.post(API_URL, json=payload)
        return response.status_code, response.json()

    # If "Predict" button clicked, get predicted grades and display in DataFrame
    if st.button("Predict"):
        status, predictions = get_prediction(loan_info)

        df = pd.DataFrame(loan_info)

        df.insert(0, "grade_category", "")
        df["grade_category"] = "Unknown"

        df.insert(0, "predicted_grade", "")
        df["predicted_grade"] = "Unknown"

        if status == 200:
            for index, prediction in predictions.items():
                new_index = int(index)

                if prediction is not None:
                    if prediction["grade_category"] is not None:
                        df.at[new_index, "grade_category"] = prediction[
                            "grade_category"
                        ]

                    if prediction["predicted_grade"] is not None:
                        df.at[new_index, "predicted_grade"] = prediction[
                            "predicted_grade"
                        ]

            df = df.sort_values(by="predicted_grade", ascending=True)
            st.dataframe(df)
        else:
            st.write(
                f"Sorry, there was an error making the prediction. Please try again later. Error message - {predictions}"
            )
