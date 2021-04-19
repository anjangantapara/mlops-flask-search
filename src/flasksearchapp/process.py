import string

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # Instantiate a TfidfVectorizer object


class ProcessData:
    list_texts = []
    text_zonder_punctuations = []
    df_tdm = pd.DataFrame()
    vectorizer = TfidfVectorizer()

    def __init__(self,search_string):
        self.search_string = search_string
        self.res = []

    @classmethod
    def set_list_texts(cls, input_list_text):
        cls.list_texts = input_list_text

    @classmethod
    def clean_text(self, text):
        """Function to remove the punctuations and get the lower case letters"""
        text_processed = text.translate(str.maketrans('', '', string.punctuation)).lower()
        return  text_processed

    @classmethod
    def text_processing(cls):
        """Function to remove the punctuations and get the lower case letters"""
        for index, text in enumerate(cls.list_texts):
            text_processed = cls.clean_text(text)
            cls.text_zonder_punctuations.append(text_processed)

    @classmethod
    def create_tdm(cls):
        X = cls.vectorizer.fit_transform(cls.text_zonder_punctuations)  # Convert the X as transposed matrix
        X = X.T.toarray()  # Create a DataFrame and set the vocabulary as the index
        cls.df_tdm = pd.DataFrame(X, index=cls.vectorizer.get_feature_names())

    def get_similar_articles(self, n_top_hits=3):
        """Function to compute similarity index"""
        search_string_clean = [ self.clean_text(self.search_string) ]
        q_vec = self.vectorizer.transform(search_string_clean).toarray().reshape(self.df_tdm.shape[0], )
        sim = {}  # Calculate the similarity
        for i in range(n_top_hits):
            print(i)
            sim[i] = np.dot(self.df_tdm.loc[:, i].values, q_vec) / np.linalg.norm(self.df_tdm.loc[:, i]) * np.linalg.norm(
                q_vec)
            print(sim[i])
        # Sort the values
        sim_sorted = sorted(sim.items(), key=lambda x: x[1],
                            reverse=True)  # Print the articles and their similarity values
        for k, v in sim_sorted:
            if v != 0.0:
                self.res.append(k)
                # print(docs[k])
        return self.res
