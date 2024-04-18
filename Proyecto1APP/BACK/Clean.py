import nltk
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class Clean:
    def __init__(self):
        self.stop_words = set(stopwords.words('spanish'))
        self.lemmatizer = WordNetLemmatizer()

    def change_characters(self, text):
        """Reemplaza algunos separadores por espacios"""
        separators = {',', '/', '.', '-', '\n', '!'}
        for sep in separators:
            text = text.replace(sep, ' ')
        return text

    def delete_wrong_words(self, words):
        """Elimina palabras de dos o menos caracteres que no se eliminaron en los stopwords"""
        return [word for word in words if len(word) > 2]
    
    def lemmatize_verbs(self, words):
        """Lematiza verbos en una lista de palabras tokenizadas"""
        lemmatized_words = []
        for word in words:
            if len(word) > 4:  # Solo lematizar palabras de longitud mayor a 4
                lemmatized_word = self.lemmatizer.lemmatize(word, pos='v')
                lemmatized_words.append(lemmatized_word)
            else:
                lemmatized_words.append(word)
        return lemmatized_words

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

    def preprocessing(self, text):
        text = self.change_characters(text)
        text = self.to_lowercase(text)
        text = self.remove_accents(text)
        words = self.filter_words(text).split()
        words = self.delete_wrong_words(words)
        words = self.remove_stopwords(words)
        words = self.lemmatize_verbs(words)
        return ' '.join(words)