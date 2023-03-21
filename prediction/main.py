import joblib
from fastapi import FastAPI

app = FastAPI()
model = joblib.load("prediction/models/step1-status_classifier.joblib")

@app.get("/")
def home():
    return {"message":"Hello with model"}