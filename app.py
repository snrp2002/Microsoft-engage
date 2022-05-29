# This program is used to generate movie ids of similar movies / recommended movies (content based)


# importing python libraries
import numpy as np
import pandas as pd
import sys

# reading necessary files
movies = pd.read_csv("new_movie_data.csv")
similarity_matrix = np.load("similarity_matrix.npz" ,"wb", encoding="bytes")

# function to find similar movies using similarity matrix
def similar_movies(movie):
    distances = similarity_matrix['arr_0'][movie_index]
    distances= sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])
    c=0
    for i in distances:
        print(movies.iloc[i[0]].movie_id)
        c+=1
        if c>=6:
            break

# generating list of movie titles
titleList=movies['original_title']
titleList = titleList.apply(lambda x:x.lower())
titleList=np.array(titleList)
titleList = titleList.tolist()

# finding the movie titles similar with the input
res = list(filter(lambda x: sys.argv[1].lower() in x, titleList))


if  len(res)>0 :    # taking the closest movie title and generating movie ids of similar movies
    movie_index = titleList.index(res[0])
    similar_movies(movie_index)
else:               # if no matching movie title found 
    print("error")