import os
import re
import string

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix


class PredictWithTfidfLogisticRegression(object):
    
    file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets.csv")  # Emplacement du dataset

    def __init__(self):
        self.df = pd.read_csv(self.file)
        self.wl = WordNetLemmatizer()  # Utiliser pour nettoyer les mots avant analyse.

        # Initialisation des variables de vectorisation (tdif) et de regression logistique (lr)
        self.tfidf_vector = TfidfVectorizer(use_idf=True)
        self.lr_tfidf = LogisticRegression(solver='liblinear', C=10, penalty='l2')

    @classmethod
    def preprocess(cls, text: str):
        text = text.lower()
        text = text.strip()

        text = re.compile('<.*?>').sub('', text)
        text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
        text = re.sub(r'\s+', ' ', text)

        return text

    def final_preprocess(self, text: str):
        return self.preprocess(text)

    def prepare_dataset(self):
        self.df['CLEAN'] = self.df['DOMAIN'].apply(lambda x: self.final_preprocess(x))

        # SPLITTING THE TRAINING DATASET INTO TRAIN AND TEST
        x_train, x_test, y_train, y_test = train_test_split(
            self.df["CLEAN"], self.df["VALUE"], test_size=0.2, shuffle=True)  # Word2Vec

        # Tf-Idf
        x_train_vectors_tfidf = self.tfidf_vector.fit_transform(x_train)
        x_test_vectors_tfidf = self.tfidf_vector.transform(x_test)

        self.lr_tfidf.fit(x_train_vectors_tfidf, y_train)  # Train model for prediction
        
        return y_test

    def ai_predict(self, values: str):
        y_test = self.prepare_dataset()
        df_test = pd.DataFrame([values] if not isinstance(values, list) else values, columns=['DOMAIN', ])

        # Pre-processing the new dataset
        df_test['CLEAN'] = df_test['DOMAIN'].apply(lambda x: self.final_preprocess(x))
        x_test = df_test['CLEAN']  # converting words to numerical data using tf-idf

        # Use the best model to predict 'identity' value for the new dataset
        x_vector = self.tfidf_vector.transform(x_test)
        y_predict = self.lr_tfidf.predict(x_vector)
        y_prob = self.lr_tfidf.predict_proba(x_vector)[:, 1]
        df_test['predict_prob'] = y_prob
        df_test['VALUE'] = y_predict
        final = df_test[['DOMAIN', 'CLEAN', 'VALUE']].reset_index(drop=True)
        
        # print(classification_report(y_test, y_predict))
        # print('Confusion Matrix:', confusion_matrix(y_test, y_predict))

        for i in range(0, final.shape[0]):
            return final["VALUE"][0]
