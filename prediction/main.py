from fastapi import FastAPI
from io import BytesIO
import pickle
import requests

# mLink = "https://github.com/baranema/test_fastapi/blob/main/prediction/models/step1-status_classifier.pkl?raw=true"
# mfile = BytesIO(requests.get(mLink).content)
# model = pickle.load(mfile)

app = FastAPI() 

@app.get("/")
def home():
    return {"message":"Hello with model"}