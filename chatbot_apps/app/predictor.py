import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
import tensorflow.contrib.learn as skflow
import MeCab

#ラベルや学習モデルはずっとかわらないので、staticで持っておくのがいいかもしれない
#一回一回読み込んでたら死ぬのでは？

class Predictor():
    tagger = MeCab.Tagger("-Ochasen")
    INDEX_CATEGORY = 0
    INDEX_ROOT_FORM = 6
    TARGET_CATEGORIES = ["名詞","動詞","形容詞","連体詞","副詞"]
    text = []

    def extract_words(self,text):
        words = []

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
        
    def execute(self,sentence):
        #データ読み込み
        m = joblib.load("app/static/app/pkl/model.pkl")
        le = joblib.load("app/static/app/pkl/le.pkl")
        
        #予測
        self.text.append(self.extract_words(sentence))
        print(self.text)
        tv = TfidfVectorizer()
        new_data = tv.transform(self.text)
        classify=m.predict(new_data)
        
        #戻り値呼び出し
        compatible_class = le.inverse_transform(classify)
        result = reply_df.query('Label == '+ str(compatible_class))
        
        print(result["Words"])
        return result["Words"]