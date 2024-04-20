import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from langdetect import detect, DetectorFactory
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV


class CleaningProcess:
    def __init__(self): 
        #nltk.download('stopwords')  
        #nltk.download('punkt')
        self.stop_words = set(stopwords.words('spanish'))
        DetectorFactory.seed = 0
        self.isTraining = True
        self.df = None

    def change_characters(self, text):
        """Reemplaza algunos separadores por espacios"""
        separators = {',', '/', '.', '-', '\n', '!'}
        for sep in separators:
            text = text.replace(sep, ' ')
        return text

    def delete_wrong_words(self, words):
        """Elimina palabras de dos o menos caracteres que no se eliminaron en los stopwords"""
        return [word for word in words if len(word) > 2]

    def filter_words(self, text):
        """Elimina caracteres innecesarios, solo quedan palabras"""
        whitelist = set("abcdefghijklmnñopqrstuvwxyz ")
        return "".join(filter(whitelist.__contains__, text))

    def remove_accents(self, text):
        """Elimina letras con tilde"""
        accents_map = {
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u'
        }
        for accented_char, unaccented_char in accents_map.items():
            text = text.replace(accented_char, unaccented_char)
        return text

    def to_lowercase(self, words):
        """Convierte strings a minúscula"""
        return words.lower()

    def remove_stopwords(self, words):
        """Remove stop words from list of tokenized words"""
        return [word for word in words if word not in self.stop_words]


    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return None

    def preprocessing(self, text):
        text = self.change_characters(text)
        text = self.to_lowercase(text)
        text = self.remove_accents(text)
        words = self.filter_words(text)
        words = word_tokenize(words)
        words = self.remove_stopwords(words)
        words = self.delete_wrong_words(words)
        return ' '.join(words)
    
    def fit(self, data, target=None):
        self.df = data
        self.df['words'] = data['Review'].apply(self.preprocessing)
        self.df['language'] = self.df['words'].apply(self.detect_language)
        self.df = self.df[self.df['language']=='es']
        print('Cleaning Done!')
        return self

    def transform(self, data):
        if isinstance(data, str):
            data = pd.DataFrame([data], columns=['Review'])
            self.isTraining = False
        elif len(data.columns) == 1:
            self.isTraining = False
        
        if not self.isTraining:
            del self.df
            self.df = data
            self.df['words'] = data['Review'].apply(self.preprocessing)
        return self

    def predict(self, df):
        return self

class Vectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.vect = None
        
    def fit(self, df, target=None):
        df = df.df
        X = self.vectorizer.fit_transform(df['words'])
        self.data = pd.DataFrame(X.todense())
        self.data['Class'] = df['Class']
        self.data.dropna(inplace=True)
        print('Vectorization Done!')
        return self

    def transform(self, df):
        if not df.isTraining:
            self.vect = self.vectorizer.transform(df.df['words'])
            self.df = df.df
        return self
    
    def predict(self, data):
        return self
    
    
class Balancer:
    def __init__(self):
        self.sm = SMOTE(random_state=42)

    def fit(self, data, target=None):
        y = data.data['Class']
        x = data.data.drop('Class', axis=1)
        self.x, self.y = self.sm.fit_resample(x, y)
        print('Balancing Done!')
        return self

    def transform(self, data):
        if data.vect is not None:
            self.vect = data.vect
            self.df = data.df
        return self

    def predict(self, data):
        return self

class Model:

    def __init__(self):
        self.report = None
        self.f1 = None
        self.recall = None
        self.precision = None
        self.model = SVC()
        C = [50, 10, 1.0, 0.1, 0.01]
        kernel = ['poly', 'rbf', 'sigmoid']
        gamma = ['scale']
        self.grid = dict(C=C, kernel=kernel, gamma=gamma)
        self.cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        
        

    def fit(self, data, target=None):
        self.model = GridSearchCV(estimator=self.model, param_grid=self.grid, n_jobs=-1, cv=self.cv, scoring='f1_weighted',error_score=0)
        X_train, X_test, Y_train, Y_test = train_test_split(data.x, data.y, test_size=0.2, random_state=42)
        self.model.fit(X_train, Y_train)
        Y_test_predictSVC = self.model.predict(X_test)
        self.report = classification_report(Y_test, Y_test_predictSVC)
        self.f1 = f1_score(Y_test, Y_test_predictSVC, average='weighted')
        self.recall = recall_score(Y_test, Y_test_predictSVC, average='weighted')
        self.precision = precision_score(Y_test, Y_test_predictSVC, average='weighted')
        print('Model Done!')

    def transform(self, data):
        return self
    
    def predict(self, data):
        data.df['Predicted'] = self.model.predict(pd.DataFrame(data.vect.todense()))
        data.df.drop('words', axis=1, inplace=True)
        data.df['Predicted'] = data.df['Predicted'].astype(int)
        return data.df