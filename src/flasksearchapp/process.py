import string
from typing import Optional, List

import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer  # Instantiate a TfidfVectorizer object

# initiating the stemmer
porter = PorterStemmer()


class SearchDocuments:
    documents = []  # contain all the documents
    documents_names = []
    processed_documents = []  # contain all the cleaned documents
    df_tdm = pd.DataFrame()  # contains vectorized matrix
    # initiating the vectorizer and setting to remove stop_words
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3),
                                 use_idf=True)  # sk-learn object containing the algo to vectorize

    def __init__(self, search_string: str)->None:
        """
        initialize instance varaibles
        :param search_string:
        :type search_string:
        """
        self.search_string = search_string
        self.search_results = []

    @classmethod
    def set_documents(cls, input_list_text: List[str]) -> None:
        """
        Function to initialize class variable documents
        :param input_list_text: list of documents
        :type input_list_text: list[str]
        """
        cls.documents = input_list_text

    @classmethod
    def set_documents_names(cls, input_list_names: List[str]) -> None:
        """
        Mehod to set documents_names
        :param input_list_names: list of doc names
        :type input_list_names: list(str)
        """
        cls.documents_names = input_list_names

    @classmethod
    def clean_document(cls, text: str) -> str:
        """Function to remove punctuations, stem words and finally convert the text into lower case
        :param text: string/text that needs to be cleaned
        :type text: str
        :return: cleaned string/text
        :rtype: str
        """
        # stop words will be removed while computing the vectorizer
        text_processed = text.translate(
            str.maketrans('', '', string.punctuation)).lower()  # removing punctuations and converting to lower case
        # tokenization
        token_words = word_tokenize(text_processed)
        # stemming below
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
        """
        Function to create tf_idf matrix
        """
        X = cls.vectorizer.fit_transform(cls.processed_documents)  # Convert the X as transposed matrix
        X = X.T.toarray()  # Create a DataFrame and set the vocabulary as the index
        cls.df_tdm = pd.DataFrame(X, index=cls.vectorizer.get_feature_names())

    def get_relevant_documents(self, n_top_hits: Optional[int] = 10) -> List[str]:
        """Function to compute similarity index
        :param n_top_hits: number of hits to show
        :type n_top_hits: int
        :return: search_results
        :rtype: list(str)
        """
        search_string_clean = [self.clean_document(self.search_string)]
        q_vec = self.vectorizer.transform(search_string_clean).toarray().reshape(self.df_tdm.shape[0], )
        sim = {}  # Calculate the similarity
        for i in range(n_top_hits):
            print(i)
            sim[i] = np.dot(self.df_tdm.loc[:, i].values, q_vec) / np.linalg.norm(
                self.df_tdm.loc[:, i]) * np.linalg.norm(q_vec)
        # Sort the values
        sim_sorted = sorted(sim.items(), key=lambda item: item[1],
                            reverse=True)  # Print the articles and their similarity values
        for k, v in sim_sorted:
            if v != 0.0:
                self.search_results.append(self.documents_names[k])
                # print(docs[k])
        return self.search_results
