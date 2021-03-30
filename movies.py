from ast import literal_eval
import pickle
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df1 = pd.read_csv('credits.csv')
df2 = pd.read_csv('movies.csv')
df1.columns = ['id', 'title', 'cast', 'crew']
df2 = df2.merge(df1, on='id')
tfidf = TfidfVectorizer(stop_words='english')

df2['overview'] = df2['overview'].fillna('')

tfidf_matrix = tfidf.fit_transform(df2['overview'])




cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
pickle.dump(cosine_sim, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))
indices = pd.Series(df2.index, index=df2['title_x']).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    return df2['title_x'].iloc[movie_indices]

