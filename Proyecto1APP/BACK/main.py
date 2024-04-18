from msilib.schema import File
import os
import sys
import csv
from joblib import load
import pandas as pd
import plotly.graph_objects as go

from io import StringIO
#from django.http import FileResponse
from fastapi import FastAPI, UploadFile, Request, requests
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


app = FastAPI()
pipeline = load('assets/Modelomejorado.joblib')
# Entrenar el modelo con el dataset


@app.get('/')
def readRoot():
    return {'Hello': 'World'}


@app.post('/predict')
def makePredictions(dataModel: DataModel):
    data_dict = dataModel.dict()
    df=pd.DataFrame([data_dict], columns=dataModel.columns())
    clean = Clean()
    df['words'] = df['Review'].apply(clean.preprocessing)
    predictions = pipeline.predict(df['words'])
    return {'predictions': predictions.tolist()}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    if file.content_type != 'text/csv':
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:

        dataframe= pd.read_csv(file.file)
        dataframe= dataframe["Review"]
        clean = Clean()
        dataframe = dataframe.apply(clean.preprocessing)
        predictions = pipeline.predict(dataframe)
        return{
            "predictions": predictions.tolist()}
        
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})
    
    


@app.post("/upload2")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    
    if file.content_type != 'text/csv':
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:
        dataframe = pd.read_csv(file.file)
        reviews = dataframe["Review"]
        clean = Clean()
        preprocessed_reviews = reviews.apply(clean.preprocessing)
      
        predictions = pipeline.predict(preprocessed_reviews)
        dataframe['Predictions'] = predictions
        print(dataframe["Predictions"])
        
        # Guardar el DataFrame modificado en un nuevo archivo CSV
        output_filename = 'predictions_' + file.filename
        output_path = os.path.join(os.getcwd(), output_filename)
        dataframe.to_csv(output_path, index=False)
        return FileResponse(output_path, media_type='text/csv', filename=output_filename)
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})




    
