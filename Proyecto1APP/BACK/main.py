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


app = FastAPI()
pipeline = load('assets/pipeline.joblib')
# Entrenar el modelo con el dataset


@app.get('/')
def readRoot():
    return {'Hello': 'World'}


@app.post('/predict')
def makePredictions(dataModel: DataModel):
    predictions = pipeline.predict(dataModel.Review)
    return {'predictions': predictions['Predicted'].tolist()}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    if file.content_type != 'text/csv':
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:

        dataframe= pd.read_csv(file.file)
        print(dataframe.head())
        predictions = pipeline.predict(dataframe)
        print(predictions)
        # Pasar predictions a un csv y devolverlo
        output = StringIO()
        predictions.to_csv(output, index=False)
        return Response(content=output.getvalue(), media_type='text/csv', headers={'Content-Disposition': f'attachment; filename=predictions_{file.filename}'})
        
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})
    
    


@app.post("/upload2")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    
    if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:
        dataframe = pd.read_csv(file.file)
      
        predictions = pipeline.predict(dataframe)
        
        # Guardar el DataFrame modificado en un nuevo archivo CSV
        output_filename = 'predictions_' + file.filename
        output_path = os.path.join(os.getcwd(), output_filename)
        dataframe.to_csv(output_path, index=False)
        return FileResponse(output_path, media_type='text/csv', filename=output_filename)
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})




    





    
