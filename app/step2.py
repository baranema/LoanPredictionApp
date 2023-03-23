import requests
import streamlit as st 
import pandas as pd 
 
API_URL = 'https://eb-loan-prediction-backend.herokuapp.com/step2_grade_prediction/'
 
def grade_pred():
    st.title('Loan Grade Prediction')
    st.write('Upload your csv file to check anticipatory grade of your loan:')
 
    st.selectbox('Input Type', ['CSV Upload'])

    uploaded_file = st.file_uploader('Upload CSV file')
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) 
        loan_info = df.to_dict(orient='records')
    else:
        loan_info = []

    def get_prediction(payload): 
        response = requests.post(API_URL, json=payload) 
        return response.status_code, response.json()
 
    if st.button('Predict'):
        status, predictions = get_prediction(loan_info)
        df = pd.DataFrame(loan_info)
        df['grade'] = "Unknown"
        
        if status == 200: 
            for index, prediction in predictions.items(): 
                new_index = int(index)
                print(prediction) 

            st.dataframe(df)
        else:
            st.write(f'Sorry, there was an error making the prediction. Please try again later. Error message - {predictions}')