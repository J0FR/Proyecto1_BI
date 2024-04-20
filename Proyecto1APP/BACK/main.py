import json
from msilib.schema import File
import os
import sys
import csv
from joblib import load
import pandas as pd
import plotly.graph_objects as go

from io import StringIO
#from django.http import FileResponse
from fastapi import FastAPI, Response, UploadFile, Request, requests
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse
from PredictionModel import Model
from Clean import Clean
from DataModel import DataModel
from fastapi import FastAPI, UploadFile, File
from io import StringIO

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
pipeline = load('assets/pipeline.joblib')
pipeline2 = load('assets/Modelomejorado.joblib')
# Entrenar el modelo con el dataset

origins = [
    'http://localhost/8000',
    "http://127.0.0.1:8000",
    'http://localhost:5173'

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/')
def readRoot():
    return {'Hello': 'World'}

@app.post('/predict')
def makePredictions(dataModel: DataModel):
    data_dict = dataModel.dict()
    df=pd.DataFrame([data_dict], columns=dataModel.columns())
    clean = Clean()
    df['words'] = df['Review'].apply(clean.preprocessing)
    predictions = pipeline2.predict(df['words'])
    return {'predictions': predictions.tolist()}

    
@app.post("/upload2")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    
    if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:
        dataframe = pd.read_csv(file.file)
        reviews = dataframe["Review"]
        clean = Clean()
        preprocessed_reviews = reviews.apply(clean.preprocessing)
      
        predictions = pipeline2.predict(preprocessed_reviews)
        dataframe['Predictions'] = predictions
        print(dataframe["Predictions"])
        
        # Guardar el DataFrame modificado en un nuevo archivo CSV
        output_filename = 'predictions_' + file.filename
        output_path = os.path.join(os.getcwd(), output_filename)
        dataframe.to_csv(output_path, index=False, sep=';')
        return FileResponse(output_path, media_type='text/csv', filename=output_filename)
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error":str(e)})
    
    
@app.post("/retrain")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    
    if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:
        dataframe = pd.read_csv(file.file)
      
        pipeline.fit(dataframe)
    
        return Response(status_code=200, headers={'Access-Control-Allow-Origin': '*'})
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})
    
    
@app.get("/report")
def get_report():
    
    answer = {
              'f1': pipeline['model'].f1, 
              'precision': pipeline['model'].precision, 
              'recall': pipeline['model'].recall}
    
    return Response(content=json.dumps(answer), media_type='application/json', headers={'Access-Control-Allow-Origin': '*'})

@app.get("/words/{id}")
def get_words(id: int):
    variables = {1: pipeline['vectorizer'].impact1,
                 2: pipeline['vectorizer'].impact2,
                 3: pipeline['vectorizer'].impact3,
                 4: pipeline['vectorizer'].impact4,
                 5: pipeline['vectorizer'].impact5}
    
    vect_array = variables[id]
    vect_array.rename(columns={'term': 'text'}, inplace=True)
    vect_array.rename(columns={'weight': 'value'}, inplace=True)
    vect_array = vect_array.to_json(orient='records')
    return Response(content=vect_array, media_type='application/json', headers={'Access-Control-Allow-Origin': '*'})
    





    





    
