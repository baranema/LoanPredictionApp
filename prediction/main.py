import joblib
from fastapi import FastAPI
import pandas as pd
from prediction.loan_classes import LoanStep1, LoanStep2

app = FastAPI()
model = joblib.load("prediction/models/step1-status_classifier.joblib")
ACCEPTED_REJECTED_MAPPING = {0: "Rejected", 1: "Accepted"}

print(type(model.named_steps['model']).__name__)

@app.get("/")
def home():
    return {"message":"Hello. This is loan acceptance prediction ;]"}

def predict_accepted_rejected(model, loans): 
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())
    
        prediction = model.predict(new_entry)
        predicted_proba = model.predict_proba(new_entry)
    
        results[i] = {
            "Loan_Acceptance": ACCEPTED_REJECTED_MAPPING[prediction[0]],
            "accepted_proba": predicted_proba[:, 1][0],
            "rejected_proba": predicted_proba[:, 0][0]
        }
        i+=1

    return results
 
@app.post("/step1_accepted_rejected_prediction/")
async def predict_accepted_rejected_query(loans: list[LoanStep1]):
    return predict_accepted_rejected(model, loans)

@app.post("/step2_grade_prediction/")
async def predict_grade_query(loan: LoanStep2):
    return {}