import string

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # Instantiate a TfidfVectorizer object
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import ReppTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
# from nltk.stem import SnowballStemmer

# initiating the stemmer
porter = PorterStemmer()

class SearchDocuments:
    documents = [] #  contain all the documents
    documents_names = []
    processed_documents = [] #  contain all the cleaned documents
    df_tdm = pd.DataFrame() # contains vectorized matrix
    # initiating the vectorizer and setting to remove stop_words
    vectorizer = TfidfVectorizer(stop_words='english',ngram_range=(1,3), use_idf=True) # sk-learn object containing the algo to vectorize

    def __init__(self,search_string):
        self.search_string = search_string
        self.search_results = []

    @classmethod
    def set_documents(cls, input_list_text):
        cls.documents = input_list_text

    @classmethod
    def set_documents_names(cls, input_list_names):
        cls.documents_names = input_list_names

    @classmethod
    def clean_document(cls, text):
        """Function to remove punctuations, stem words and finally convert the text into lower case"""
        # stop words will be removed while computing the vectorizer
        text_processed = text.translate(str.maketrans('', '', string.punctuation)).lower() # removing punctuations and converting to lower case
        # tokenization
        token_words = word_tokenize(text_processed)
        #stemming below
        stem_sentence = []
        for word in token_words:
            stem_sentence.append(porter.stem(word))
            stem_sentence.append(" ")
        return "".join(stem_sentence)


    # @classmethod
    # def clean_text(self, text):
    #     """Function to remove the punctuations and turn the text into lower case"""
    #     text_processed = text.translate(str.maketrans('', '', string.punctuation)).lower()
    #     return  text_processed

    @classmethod
    def clean_all_documents(cls):
        """Function to remove the punctuations and get the lower case letters"""
        for index, text in enumerate(cls.documents):
            text_processed = cls.clean_document(text)
            cls.processed_documents.append(text_processed)

    @classmethod
    def create_tdm(cls):
        X = cls.vectorizer.fit_transform(cls.processed_documents)  # Convert the X as transposed matrix
        X = X.T.toarray()  # Create a DataFrame and set the vocabulary as the index
        cls.df_tdm = pd.DataFrame(X, index=cls.vectorizer.get_feature_names())

    def get_relevant_documents(self, n_top_hits=10):
        """Function to compute similarity index"""
        search_string_clean = [self.clean_document(self.search_string)]
        q_vec = self.vectorizer.transform(search_string_clean).toarray().reshape(self.df_tdm.shape[0], )
        sim = {}  # Calculate the similarity
        for i in range(n_top_hits):
            print(i)
            sim[i] = np.dot(self.df_tdm.loc[:, i].values, q_vec) / np.linalg.norm(self.df_tdm.loc[:, i]) * np.linalg.norm(q_vec)
        # Sort the values
        sim_sorted = sorted(sim.items(), key=lambda item: item[1], reverse=True)  # Print the articles and their similarity values
        for k, v in sim_sorted:
            if v != 0.0:
                self.search_results.append(self.documents_names[k])
                # print(docs[k])
        return self.search_results
