from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

new_df = pd.read_parquet("./datasets/movies_model_final.parquet")

cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(new_df["tags"]).toarray()

similarity = cosine_similarity(vectors)

# def recommend(movie):
#     movie_index = new_df[new_df["title"] == movie].index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
#     for i in movie_list:
#         print(new_df.iloc[i[0]].title)
#         # print(i[0])
#     # return

# def recommend(movie):
#     movie_index = new_df[new_df["title"] == movie].index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
#     pel = []
#     for i in movie_list:
#         list_pel = new_df.iloc[i[0]].title
#         pel.append(list_pel)
#         # print(i[0])
#     return pel


def recommend(movie):
    movie_index = new_df[new_df["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    pel = []
    for i in movie_list:
        list_pel = new_df.iloc[i[0]].title
        pel.append(list_pel)
        # print(i[0])
    return pel

# recommend("Lethal Weapon")



