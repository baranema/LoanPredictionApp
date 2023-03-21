import urllib.request
import pickle
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

model = pickle.load(urllib.request.urlopen("https://storage.cloud.google.com/modelstep1/step1-status_classifier.joblib"))
 
@app.get("/")
def home():
    return {"message":"Hello with model"}
