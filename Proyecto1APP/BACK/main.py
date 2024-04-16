from typing import Optional
from fastapi import FastAPI
import pandas as pd
import PredictionModel

app = FastAPI()

@app.get('/')
def readRoot():
    return {'Hello': 'World'}

@app.get('/items/{itemID}')
def readItem(itemID, q=None):
    return {'itemID': itemID, 'q': q}

@app.post('/predict')
def makePredictions(dataModel):
    df = pd.DataFrame(dataModel.dict(), columns='')
    model = PredictionModel()
    return model.makePredictions(df)