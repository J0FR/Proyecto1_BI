import joblib
import pandas as pd
from Pipes import CleaningProcess, Vectorizer, Balancer, Model
# Load the joblib file

from joblib import dump, load
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('cleaner', CleaningProcess()),
    ('vectorizer', Vectorizer()),
    ('balancer', Balancer()),
    ('model', Model())
])

dftest=pd.read_csv("Proyecto1APP/BACK/assets/entrenamiento_estudiantes.csv")
pd.options.mode.chained_assignment = None

print("Entrenando modelo")
pipeline.fit(dftest)  # Apply the transformation to the dataframe

dump(pipeline, 'Proyecto1APP/BACK/assets/pipeline.joblib', compress=True)
# print("Modelo guardado")

