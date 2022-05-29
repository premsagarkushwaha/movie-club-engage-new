import pandas as pd 
import ast
import numpy as np
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import contractions
import nltk
dt = pd.read_csv("dataset/new_data_movie.csv")

dt['tagline'] = dt['tagline'].fillna('')
dt['description'] = dt['overview'] + dt['tagline']+dt['genres'].map(str) + dt['keywords'].map(str)
dt['description'] = dt['description'].fillna('')


tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(dt['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
dt = dt.reset_index()
titles = dt['title']
indices = pd.Series(dt.index, index=dt['title'])
reader = Reader()
# ratings = pd.read_csv('dataset/rating_small.csv') # large dataset downloaded from kaggle 
ratings = pd.read_csv('dataset/file_names3.csv') # small datset that will generate through this application from user rating to use in this model 
ratings.head()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
svd = SVD()
trainset = data.build_full_trainset()
svd.fit(trainset)
def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan
id_map = pd.read_csv('dataset/link_small2.csv')[['movieId', 'tmdbId']]
id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(dt[['title', 'id']], on='id').set_index('title')
indices_map = id_map.set_index('id')
def hybrid(userId, title):
    try:
        idx = indices[title]
        tmdbId = id_map.loc[title]['id']
        # movie_id = id_map.loc[title]['movieId']
        sim_scores = list(enumerate(cosine_sim[int(idx)]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]
        movies = dt.iloc[movie_indices][['title', 'vote_count', 'vote_average','year', 'id']]
        est = []
        for x in list(movies['id']):
            try:
                est.append(svd.predict(userId, indices_map.loc[x]['movieId']).est)
            except:
                est.append(0)
        movies['est'] = est
        movies = movies.sort_values('est', ascending=False)
        return list(movies.head(10)['title'])
    except:
        return movie_recommender(title.lower())

# model 2

df = pd.read_csv("dataset/nltk_data.csv")
stop_words = nltk.corpus.stopwords.words('english') # fetching stopwords 
def normalize_document(doc):
    doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I|re.A)
    doc = doc.lower()
    doc = doc.strip()
    doc = contractions.fix(doc)
    tokens = nltk.word_tokenize(doc)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    doc = ' '.join(filtered_tokens)
    return doc
normalize_corpus = np.vectorize(normalize_document)
norm_corpus = normalize_corpus(list(df['description']))
tf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
tfidf_matrix = tf.fit_transform(norm_corpus)
tfidf_matrix.shape
doc_sim = cosine_similarity(tfidf_matrix)
doc_sim_df = pd.DataFrame(doc_sim)
movies_list = df['title'].values
def movie_recommender(movie_title, movies=movies_list, doc_sims=doc_sim_df):
    movie_idx = np.where(movies == movie_title)[0][0]
    movie_similarities = doc_sims.iloc[movie_idx].values
    similar_movie_idxs = np.argsort(-movie_similarities)[1:11]
    similar_movies = movies[similar_movie_idxs]
    return similar_movies

