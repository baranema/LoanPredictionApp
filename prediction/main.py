import joblib
from fastapi import FastAPI
from prediction.loan_classes import LoanStep1, LoanStep2, LoanStep3, LoanStep4
from prediction.predictions import (
    predict_accepted_rejected,
    predict_grade,
    predict_subgrade,
    predict_int_rate,
)

app = FastAPI()

# Load pre-trained models
model_step1 = joblib.load("prediction/models/step1-status_classifier.joblib")
model_step2 = joblib.load("prediction/models/step2-grade_classifier.joblib")
model_step3 = joblib.load("prediction/models/step3-subgrade_classifier.joblib")
model_step4 = joblib.load("prediction/models/step4-int_rate_pred.joblib")


@app.get("/")
def home():
    """
    A simple endpoint to verify if the server is running.
    """
    return {"message": "Hello. This is loan acceptance prediction!"}


@app.post("/step1_accepted_rejected_prediction/")
async def predict_accepted_rejected_query(loans: list[LoanStep1]):
    """
    Predicts whether a loan application will be accepted or rejected based on step 1 data.

    Parameters:
    loans (list[LoanStep1]): A list of LoanStep1 objects containing borrower's personal information.

    Returns:
    dict: A dictionary containing predicted loan status (0 or 1) for each loan in the input list.
    """
    return predict_accepted_rejected(model_step1, loans)


@app.post("/step2_grade_prediction/")
async def predict_grade_query(loans: list[LoanStep2]):
    """
    Predicts the grade of a loan application based on step 2 data.

    Parameters:
    loans (list[LoanStep2]): A list of LoanStep2 objects containing borrower's financial information.

    Returns:
    dict: A dictionary containing predicted loan grades (A, B, C, D, E, F or G) for each loan in the input list.
    """
    return predict_grade(model_step2, loans)


@app.post("/step3_subgrade_prediction/")
async def predict_subgrade_query(loans: list[LoanStep3]):
    """
    Predicts the subgrade of a loan application based on step 3 data.

    Parameters:
    loans (list[LoanStep3]): A list of LoanStep3 objects containing borrower's credit information.

    Returns:
    dict: A dictionary containing predicted loan subgrades (A, B, C, D, E, F or G) x (1 to 5) for each loan in the input list.
    """
    return predict_subgrade(model_step3, loans)


@app.post("/step4_int_rate_prediction/")
async def predict_int_rate_query(loans: list[LoanStep4]):
    """
    Predicts the interest rate of a loan application based on step 4 data.

    Parameters:
    loans (list[LoanStep4]): A list of LoanStep4 objects containing borrower's loan information.

    Returns:
    dict: A dictionary containing predicted loan interest rates for each loan in the input list.
    """
    return predict_int_rate(model_step4, loans)
