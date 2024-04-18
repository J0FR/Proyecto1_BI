import re
import sys
import os
import pandas as pd
import joblib as jb

from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize.casual import casual_tokenize
from nltk.stem.snowball import SnowballStemmer



class Model:

    def __init__(self):
        self.model = jb.load("assets/Modelomejorado.joblib")

    def make_predictions(self, data):
        result = self.model.predict(data)
        return result    