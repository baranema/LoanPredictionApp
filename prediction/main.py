import joblib
from fastapi import FastAPI
import joblib
import pandas as pd
from fastapi import FastAPI
from step1_loan import LoanStep1

app = FastAPI()
model = joblib.load("prediction/models/step1-status_classifier.joblib")

@app.get("/")
def home():
    return {"message":"Hello with model"}