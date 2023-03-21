import joblib
from fastapi import FastAPI
import pandas as pd
from prediction.step1_loan import LoanStep1

app = FastAPI()
model = joblib.load("prediction/models/step1-status_classifier.joblib")
ACCEPTED_REJECTED_MAPPING = {0: "Rejected", 1: "Accepted"}

@app.get("/")
def home():
    return {"message":"Hello with model!!!"}

def predict_accepted_rejected(model, entry):
    """Get data from entry object as a dict"""
    new_entry = pd.DataFrame.from_dict(entry.get_entry_dict())

    """ Predict new data based on threshold """
    prediction = model.predict(new_entry)
    predicted_proba = model.predict_proba(new_entry)
 
    return {
        "Loan_Acceptance": ACCEPTED_REJECTED_MAPPING[prediction[0]],
        "accepted_proba": predicted_proba[:, 1][0],
        "rejected_proba": predicted_proba[:, 0][0]
    }
