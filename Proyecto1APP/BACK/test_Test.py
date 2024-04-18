import joblib
import pandas as pd

# Load the joblib model
model = joblib.load('Proyecto1APP/BACK/assets/pipeline.joblib')
dftest=pd.read_csv("Proyecto1APP/BACK/assets/particion_prueba_estudiantes(1).csv")

model.predict(dftest).to_csv('Proyecto1APP/BACK/assets/predictions.csv', index=False)