import string

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # Instantiate a TfidfVectorizer object


def text_processing(list_texts):
    """Function to remove the punctuations and get the lower case letters"""
    text_zonder_punctuations = []
    for index, text in enumerate(list_texts):
        text_processed = text.translate(str.maketrans('', '', string.punctuation)).lower()
        text_zonder_punctuations.append(text_processed)
    return text_zonder_punctuations


def create_tdm(list_texts):
    vectorizer = TfidfVectorizer()  # It fits the data and transform it as a vector
    X = vectorizer.fit_transform(list_texts)  # Convert the X as transposed matrix
    X = X.T.toarray()  # Create a DataFrame and set the vocabulary as the index
    df = pd.DataFrame(X, index=vectorizer.get_feature_names())
    return df, vectorizer


def get_similar_articles(search_string, df_tdm, vectorizer):
    """Function to compute similarity index"""
    search_string = [search_string]
    search_string = text_processing(search_string)
    q_vec = vectorizer.transform(search_string).toarray().reshape(df_tdm.shape[0], )
    sim = {}  # Calculate the similarity
    for i in range(10):
        print(i)
        sim[i] = np.dot(df_tdm.loc[:, i].values, q_vec) / np.linalg.norm(df_tdm.loc[:, i]) * np.linalg.norm(q_vec)
        print(sim[i])
    # Sort the values
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)  # Print the articles and their similarity values
    res = []
    for k, v in sim_sorted:
        if v != 0.0:
            res.append(k)
            # print(docs[k])
    return res
