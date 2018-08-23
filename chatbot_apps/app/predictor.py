import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
import tensorflow.contrib.learn as skflow
import Mecab

class Predictor(sentence):
    tagger = MeCab.Tagger("-Ochasen")
    INDEX_CATEGORY = 0
    INDEX_ROOT_FORM = 6
    TARGET_CATEGORIES = ["名詞","動詞","形容詞","連体詞","副詞"]

    def __init__(self):
        self.text = []        
        self.words = []
            
    def execute(self,sentence):
        cv = TfidfVectorizer(analyzer=extract_words)
        text.append(sentence)
        new_data = cv.transform(text)
        classify=m.predict(new_data)
        compatible_class = le.inverse_transform(classify)
        result = reply_df.query('Label == '+ str(compatible_class))
        return result["Words"]

    def extract_words(self,text):
        if not text:
            return []

        node = self.tagger.parseToNode(text)
        while node:
            features = node.feature.split(',')
            if features[self.INDEX_CATEGORY] in self.TARGET_CATEGORIES:
                if features[self.INDEX_ROOT_FORM] == "*":
                    words.append(node.surface)
                else:
                    words.append(features[self.INDEX_ROOT_FORM])

            node = node.next

        return words