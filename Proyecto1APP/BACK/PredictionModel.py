from joblib import load

class Model:

    def __init__(self):
        self.model = load('assets/modelo.joblib')
        
    
    def makePredictions(self, data):
        return self.model.predict(data)