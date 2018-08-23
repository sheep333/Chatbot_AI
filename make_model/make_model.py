# -*- coding: utf-8 -*-
from google.colab import files
import pandas as pd
import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

#################
#---データ作成---#
#################

#50音データ読み込み

#reply.csvのインポート
reply_df = pd.read_csv('reply.csv')
df = pd.read_csv('data.csv')

#--形態素解析してTF-IDFで特徴語を抽出して辞書化--#
#必要なメンバ
text=[]
classify=[]
words=[]
dict=[]

#辞書の読込み
tagger = MeCab.Tagger("-Ochasen")

#Mecabで単語単位に分けるクラス
class WordDividor:
    INDEX_CATEGORY = 0 #品詞が入っている
    INDEX_ROOT_FORM = 6 #形態素の基本形が入っている(ex.食べ⇒「食べる」)
    TARGET_CATEGORIES = ["名詞","動詞","形容詞","連体詞","副詞"]

    def __init__(self, dictionary="mecabrc"):
        self.dictionary = dictionary
        self.tagger = MeCab.Tagger(self.dictionary)
        
    def extract_words(self, text):
        if not text:
            return []

        words = []
        
        node = self.tagger.parseToNode(text)
        #node.featureで表層系の形態素解析をしたカンマ区切りの値が戻ってくる(ex.「名詞,副詞可能,*,*,*,*,今日,キョウ,キョー」)
        while node:
            features = node.feature.split(',')
            print(features)
            if features[self.INDEX_CATEGORY] in self.TARGET_CATEGORIES:
                if features[self.INDEX_ROOT_FORM] == "*":
                    words.append(node.surface)
                else:
                    words.append(features[self.INDEX_ROOT_FORM])

            node = node.next

        return words

################
#--Modelの作成--#
#################

#ファイルから読み込み
X=None # 学習データ
Y=None # ラベルデータ

sentence = df["sentence"]
label = df["label"]

#ラベリング(labelを連番する)
le = LabelEncoder()
classify_label=le.fit_transform(label)

#sentenceを単語に分解(analyzerにextract_wordsの戻り値を設定)
wd = WordDividor()
#ngram(ランダムな長さの文字列)の配列を返す関数を引数にする
cv = TfidfVectorizer(analyzer=wd.extract_words)
classify_dictionary = cv.fit_transform(sentence) #文章ごとに辞書化

#単語の出現を辞書の番号でカウント(通常のベクトル)
appearance = classify_dictionary.toarray()

#カテゴリを数値に変更
model = MLPClassifier(hidden_layer_sizes=(200,300,),early_stopping=True,max_iter=300,activation='relu',solver='adam')
data = model.fit(classify_dictionary,classify_label)

"""
#できるならRNNで前後の文脈も判断したい
#RNNで渡すには単語ごとに分解して覚えている数を指定して、次の文に移ったらリセットのような形で関連性を学習させればよさそう
#classifier = skflow.TensorFlowRNNClassifier(rnn_size=EMBEDDING_SIZE, 
#    n_classes=15, cell_type='gru', input_op_fn=input_op_fn,
#    num_layers=1, bidirectional=False, sequence_length=None,
#    steps=1000, optimizer='Adam', learning_rate=0.01, continue_training=True)
"""

model = classifier.fit(classify_dictionary,classify_label)

#modelの保存と呼び出し
joblib.dump(model, 'model.pkl')
joblib.dump(appearance,'appear.pkl')
joblib.dump(le, 'le.pkl')

m = joblib.load('model.pkl')
a = joblib.load('appear.pkl')
le = joblib.load('le.pkl')

#予測
a="かしこい？"

text=[]
text.append(a)
new_data = cv.transform(text)
classify=m.predict(new_data)
compatible_class = le.inverse_transform(classify)

print(compatible_class)

for (c,x) in  enumerate(m.predict_proba(new_data)[0]):
    print(":".join([str(c), str(x)]))
    
print(reply_df['Label'].query('Label == '+ str(compatible_class)))


"""Kerasを使ってみたい
#################
#--モデルの作成--#
#################
#Kerasでのmodelの作成
model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))#隠れ層
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.summary()


#--モデルのコンパイル--#
model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
#--学習--#
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=40,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)

#--学習の状況を表示--#
results = model.evaluate(test_data, test_labels)
print(results)
"""