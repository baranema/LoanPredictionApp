import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI()
model = joblib.load("models/step1-status_classifier.joblib")


@app.get("/")
def home():
    return {"message":"Hello This is loan Prediction"}
