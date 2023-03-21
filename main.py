import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI()
model = joblib.load("https://storage.cloud.google.com/modelstep1/step1-status_classifier.joblib")
 
@app.get("/")
def home():
    return {"message":"Hello with model"}
