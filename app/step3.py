# Import the necessary packages
import requests
import streamlit as st
import pandas as pd

API_URL = "https://eb-loan-prediction-backend.herokuapp.com/step3_subgrade_prediction/"


def subgrade_pred():
    # Sets the title and description for the Streamlit app
    st.title("Loan Subrade Prediction")
    st.write("Upload your csv file to check anticipatory subgrade of your loan:")

    # Displays the file upload widget
    st.selectbox("Input Type", ["CSV Upload"])
    uploaded_file = st.file_uploader("Upload CSV file")

    # If a file is uploaded, reads the CSV file and converts it to a dictionary
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        loan_info = df.to_dict(orient="records")
    else:
        loan_info = []

    # Sends the loan_info dictionary as JSON payload to the Heroku app's subgrade prediction endpoint
    def get_prediction(payload):
        response = requests.post(API_URL, json=payload)
        return response.status_code, response.json()

    # Displays the predicted subgrades in a table format
    if st.button("Predict"):
        status, predictions = get_prediction(loan_info)
        df = pd.DataFrame(loan_info)

        df.insert(0, "subgrade_category", "")
        df["subgrade_category"] = "Unknown"

        df.insert(0, "predicted_subgrade", "")
        df["predicted_subgrade"] = "Unknown"

        if status == 200:
            for index, prediction in predictions.items():
                new_index = int(index)

                if prediction is not None:
                    if prediction["subgrade_category"] is not None:
                        df.at[new_index, "subgrade_category"] = prediction[
                            "subgrade_category"
                        ]

                    if prediction["predicted_subgrade"] is not None:
                        df.at[new_index, "predicted_subgrade"] = prediction[
                            "predicted_subgrade"
                        ]

            df = df.sort_values(by="predicted_subgrade", ascending=True)
            st.dataframe(df)

        else:
            st.write(
                f"Sorry, there was an error making the prediction. Please try again later. Error message - {predictions}"
            )
