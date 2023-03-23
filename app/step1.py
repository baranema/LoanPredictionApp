import requests
import streamlit as st 
import pandas as pd 

# Define the API endpoint URL
API_URL = 'https://eb-loan-prediction-backend.herokuapp.com/step1_accepted_rejected_prediction/'

def acceptance_val(val):
    color = '#1d915b' if val == "ACCEPTED" else '#911d2d'
    return f'background-color: {color}'

# Define the streamlit app
def acc_pred(): 
    st.title('Loan Acceptance Prediction')
    st.write('Enter the following details to check if your loan application will be accepted or rejected:')

    # Define input fields
    input_type = st.selectbox('Input Type', ['Manual Input', 'CSV Upload'])

    if input_type == 'Manual Input':
        # Define input fields
        loan_amnt = st.number_input('Loan Amount', min_value=1.0, step=0.00001, format="%.5f")
        dti = st.number_input('Debt-to-Income Ratio', min_value=0.0, step=0.00001, format="%.5f")
        emp_length = st.selectbox('Employment Length', ['< 1 year', '1 year', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', '8 years', '9 years', '10+ years'])
        purpose = st.selectbox('Loan Purpose', ['debt_consolidation', 'small_business', 'home_improvement', 'major_purchase', 'credit_card', 'other', 'house', 'vacation', 'car', 'medical', 'moving', 'renewable_energy', 'wedding', 'educational'])

        loan_info = [{
            'loan_amnt': loan_amnt,
            'dti': dti,
            'emp_length': emp_length,
            'purpose': purpose
        }]
    else:
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
        df['acceptance'] = "Unknown"
        
        if status == 200: 
            for index, prediction in predictions.items(): 
                new_index = int(index)
                if prediction is not None:
                    if prediction['Loan_Acceptance'] == 'Accepted': 
                        df.at[new_index, 'acceptance']= "ACCEPTED" 
                    elif prediction['Loan_Acceptance'] == 'Rejected':
                        df.at[new_index, 'acceptance']= "REJECTED"
             
            st.dataframe(df.style.applymap(acceptance_val, subset=['acceptance'])) 
        else:
            st.write(f'Sorry, there was an error making the prediction. Please try again later. Error message - {predictions}')