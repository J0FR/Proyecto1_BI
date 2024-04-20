import joblib
import pandas as pd

# Load the joblib model
model = joblib.load('Proyecto1APP/BACK/assets/pipeline.joblib')

print(model['vectorizer'].impact1)