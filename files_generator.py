# This python program is used to generate two files :
#   1. new_movie_data.csv       -> a file containing the processed data
#   2. similarity_matrix.npz    -> a file containing the cosine similarity matrix


# importing python libraries
import numpy as np
import pandas as pd
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import savez_compressed

# reading necessary files
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# basic data processing
movies = movies.merge(credits,on='title')
movies = movies[['movie_id','original_title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

# this function is used to extract the names of genres and keywords
def convert(obj):
    li = []
    for i in ast.literal_eval(obj):
        li.append(i['name'])
    return li
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


# this function is used to extract the names of top three casts
def convert_cast(obj):
    li = []
    c=0
    for i in ast.literal_eval(obj):
        li.append(i['name'])
        c+=1
        if c>=3:
            break
    return li
movies['cast'] = movies['cast'].apply(convert_cast)

# this function is used to extract the name of director
def convert_crew(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            l.append(i['name'])
            break
    return l
movies['crew'] = movies['crew'].apply(convert_crew)

# coverting overview string into list
movies['overview']=movies['overview'].apply(lambda x : x.split())

# removing white spaces
movies['genres']=movies['genres'].apply(lambda x : [i.replace(" ","") for i in x])
movies['overview']=movies['overview'].apply(lambda x : [i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x : [i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x : [i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x : [i.replace(" ","") for i in x])

# creating 'tag', which will be used to find similarity
movies['tag'] = movies['genres'] + movies['overview'] + movies['keywords'] + movies['cast'] + movies['crew']

# creating a new data base
new_df = movies[['movie_id','original_title','tag']]

# covering tag field into lowercase string
new_df['tag'] = new_df['tag'].apply(lambda x:" ".join(x))
new_df['tag'] = new_df['tag'].apply(lambda x:x.lower())

# stemming the tag data
ps = PorterStemmer()
def stem_text(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
new_df['tag']=new_df['tag'].apply(stem_text)


# vectorizing tag data
cv = CountVectorizer(max_features=5000,stop_words="english")
vectors = cv.fit_transform(new_df['tag']).toarray()

# generating cosine similarity matrix
similarity_matrix = cosine_similarity(vectors)

# storing new database and similarity matrix in files
new_df.to_csv("new_movie_data.csv")
savez_compressed("similarity_matrix.npz",similarity_matrix)