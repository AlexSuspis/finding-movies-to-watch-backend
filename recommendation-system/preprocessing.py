import loader, saver
import utils
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import numpy as np
import pandas as pd


def preprocess_movies():

	movies_df = loader.load_original_movies_locally()
	print(movies_df.columns)

	#split genres into a list
	movies_df['genres'] =  movies_df['genres'].apply(lambda x: x.replace("|", " "))
	# print(movies_df)

	#clean movie titles
	movies_df['clean_title'] = movies_df['title'].apply(lambda x: utils.clean_string(x))
	# print(movies_df)

	#countries
	movies_df['countries'] = movies_df['title'].apply(lambda x: utils.get_random_countries())
	# print(movies_df)

	#providers	
	movies_df['providers'] = movies_df['title'].apply(lambda x: utils.get_random_providers())
	# print(movies_df)

	#Inspired by: https://medium.com/geekculture/creating-content-based-movie-recommender-with-python-7f7d1b739c63
	movies_df['genres'] = movies_df['genres'].str.replace('Sci-Fi', "SciFi")
	movies_df['genres'] = movies_df['genres'].str.replace('Film-Noir', "FilmNoir")

	#split genres into a list
	movies_df['genres'] =  movies_df['genres'].apply(lambda x: x.split())
	# print(movies_df['genres'])

	#save locally and to database		
	saver.save_preprocessed_movies_locally(movies_df)
	# saver.post_preprocessed_movies_to_db(movies_df)


def compute_similarity_matrix():
	np.set_printoptions(threshold=np.inf)

	movies_df = loader.load_processed_movies_locally()

	features = movies_df[['movieId','genres']]
	print(features)
	# features.set_index('movieId', inplace=True)
	# print(features)

	features['genres'] = features['genres'].apply(lambda x: ''.join(x))
	# print(features['genres'])

	#Inspired by: https://medium.com/geekculture/creating-content-based-movie-recommender-with-python-7f7d1b739c63
	tfidf = TfidfVectorizer(stop_words='english')
	tfidf_matrix = tfidf.fit_transform(features['genres'])

	#Check that movie with only 1 genre has that genre's tfidf value to 1 (most important value in describing the document)
	# print(tfidf_matrix[4,:])

	similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
	movieIds = movies_df['movieId'].values
	sim_mat_df = pd.DataFrame(data=similarity_matrix, columns=movieIds, index=movieIds)
	print(sim_mat_df)

	saver.save_similarity_matrix_locally(sim_mat_df)

def explore_datasets():
	small_movies_df = loader.load_original_movies_locally()
	big_movies_df = pd.read_csv('input/big_dataset/movies_metadata')
	print(small_movies_df)
	print(big_movies_df)

explore_datasets()
# preprocess_movies()
# compute_similarity_matrix()