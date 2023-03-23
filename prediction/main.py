import joblib
from fastapi import FastAPI 
from prediction.loan_classes import LoanStep1, LoanStep2, LoanStep3
from prediction.predictions import predict_accepted_rejected, predict_grade, predict_subgrade

app = FastAPI()
model_step1 = joblib.load("prediction/models/step1-status_classifier.joblib")
model_step2 = joblib.load("prediction/models/step2-grade_classifier.joblib")
model_step3 = joblib.load("prediction/models/step3-subgrade_classifier.joblib")

@app.get("/")
def home():
    return {"message":"Hello. This is loan acceptance prediction!"}

@app.post("/step1_accepted_rejected_prediction/")
async def predict_accepted_rejected_query(loans: list[LoanStep1]):
    return predict_accepted_rejected(model_step1, loans)

@app.post("/step2_grade_prediction/")
async def predict_grade_query(loans: list[LoanStep2]):
    return predict_grade(model_step2, loans)

@app.post("/step3_subgrade_prediction/")
async def predict_subgrade_query(loans: list[LoanStep3]): 
    return predict_subgrade(model_step3, loans)