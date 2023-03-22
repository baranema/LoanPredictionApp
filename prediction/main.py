import joblib
from fastapi import FastAPI
import pandas as pd
from prediction.step1_loan import LoanStep1

app = FastAPI()
model = joblib.load("prediction/models/step1-status_classifier.joblib")
ACCEPTED_REJECTED_MAPPING = {0: "Rejected", 1: "Accepted"}

@app.get("/")
def home():
    return {"message":"Hello. This is loan acceptance prediction :)"}

def predict_accepted_rejected(model, entry): 
    new_entry = pd.DataFrame.from_dict(entry.get_entry_dict())
 
    prediction = model.predict(new_entry)
    predicted_proba = model.predict_proba(new_entry)
 
    return {
        "Loan_Acceptance": ACCEPTED_REJECTED_MAPPING[prediction[0]],
        "accepted_proba": predicted_proba[:, 1][0],
        "rejected_proba": predicted_proba[:, 0][0]
    }
 
@app.post("/step1_accepted_rejected_prediction/")
async def predict_accepted_rejected_query(loan: LoanStep1):
    return predict_accepted_rejected(model, loan)