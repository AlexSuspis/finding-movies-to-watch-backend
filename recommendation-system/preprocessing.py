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

	movies_df.drop_duplicates(subset='title', inplace=True)

	#save locally and to database		
	saver.save_preprocessed_movies_locally(movies_df)
	saver.post_preprocessed_movies_to_db(movies_df)
	
	return


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

	big_movies_df = pd.read_csv('./input/big_dataset/movies_metadata.csv')
	big_movies_df = big_movies_df[['title', 'release_date','genres', 'overview']]

	#count number of records with NaN release_date
	# is_nan_release_date = big_movies_df['release_date'].isna()
	# num_nan_release_date = is_nan_release_date.sum()
	# print(is_nan_release_date)
	# movies_with_nan_release_date = big_movies_df[is_nan_release_date]['title'].values
	# print(movies_with_nan_release_date)

	#filter out records which do not have a release date
	is_not_nan_release_date = big_movies_df['release_date'].notna()
	filtered_big_movies_df = big_movies_df[is_not_nan_release_date]
	# print(filtered_big_movies_df)

	#filter out records with invalid release dates
	invalid_dates = filtered_big_movies_df['release_date'].apply(utils.is_invalid_date_format)
	records_with_invalid_dates = filtered_big_movies_df[invalid_dates]
	print("Number of records with invalid dates in big movies",records_with_invalid_dates.sum())
	filtered_big_movies_df = filtered_big_movies_df[~invalid_dates]

	#extract year from 'release_date'
	filtered_big_movies_df['year'] = filtered_big_movies_df['release_date'].apply(utils.get_year_from_date)

	#get clean_title so we can merge with small movies dataset
	filtered_big_movies_df['clean_title'] = filtered_big_movies_df.apply(lambda row: utils.clean_string(row['title']) + str(row['year']), axis=1)

	#drop duplicates
	filtered_big_movies_df.drop_duplicates(subset='title', inplace=True)

	#import small dataset so we can merge
	small_processed_movies_df = loader.load_processed_movies_locally()
	print(small_processed_movies_df.shape)
	print('Number of NaN in big movies overview column: ' + str(filtered_big_movies_df['overview'].isna().sum()))
	print(small_processed_movies_df.shape)

	#merge
	merged_df = small_processed_movies_df.merge(filtered_big_movies_df[['overview','year','clean_title']], how='left', left_on='clean_title', right_on='clean_title')
	merged_df.drop_duplicates(inplace=True)
	print("Number of NaN in merged movies overview column: " + str(merged_df['overview'].isna().sum()))

	print(merged_df.shape)


preprocess_movies()
explore_datasets()
# compute_similarity_matrix()