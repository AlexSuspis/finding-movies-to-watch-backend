import pymongo
import pandas as pd
import pickle
import numpy as np



uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']

<<<<<<< HEAD
serverRequest = False
if(serverRequest):
	filename = './recommendation-system/input/small_dataset/movies.csv'
else:	
	filename = './input/small_dataset/movies.csv'

def get_movies_from_db():
	movies = db.original_movies.find()
	movies_df = pd.DataFrame(movies).drop(columns=['_id'])
	return movies_df

def load_movies_locally():
	movies_df = pd.read_csv(filename)
	return movies_df

def load_ratings_locally():
	ratings_df = pd.read_csv(filename)
	ratings_df.drop(columns=['timestamp'], inplace=True)
	return ratings_df

=======
serverRequest = True
# serverRequest = False
if(serverRequest == True):
	original_movies_path = './recommendation-system/input/small_dataset/movies.csv'
	processed_movies_path = './recommendation-system/processed-data/movies_processed.csv'
	ratings_path = './recommendation-system/input/small_dataset/ratings.csv'
	knn_model_path = './recommendation-system/knn_model.sav'
	final_df_path = './recommendation-system/final_df'
	similarity_matrix_path = './recommendation-system/processed-data/similarity_matrix.dat'

else:	
	original_movies_path = './input/small_dataset/movies.csv'
	processed_movies_path = './processed-data/movies_processed.csv'
	ratings_path = './input/small_dataset/ratings.csv'
	knn_model_path = './knn_model.sav'
	final_df_path = './final_df'
	similarity_matrix_path = './processed-data/similarity_matrix.dat'

def load_processed_movies_locally():
	movies_df = pd.read_csv(processed_movies_path)	
	return movies_df


def load_original_movies_locally():
	movies_df = pd.read_csv(original_movies_path)
	return movies_df

def load_original_ratings_locally():
	ratings_df = pd.read_csv(ratings_path)
	ratings_df.drop(columns=['timestamp'], inplace=True)
	return ratings_df

def load_similarity_matrix_locally():
	try:
		similarity_matrix = pickle.load(open(similarity_matrix_path,'rb'))
		return similarity_matrix
	except:
		print('Error occurred when attempting to load similarity_matrix!')
		


def get_movies_from_db():
	movies = db.original_movies.find()
	movies_df = pd.DataFrame(movies).drop(columns=['_id'])
	return movies_df

>>>>>>> recommender-system-2.0
def get_ratings_from_db():
	ratings = db.original_ratings.find()
	ratings_df = pd.DataFrame(ratings).drop(columns=['_id'])
	return ratings_df

def load_knn_model_locally():
<<<<<<< HEAD
	if serverRequest:
		path = './recommendation-system/knn_model.sav'
	else: 
		path = './knn_model.sav'

	knn_model = pickle.load(open(filename, 'rb'))
	return knn_model

def load_final_df_locally():
	if serverRequest:
		path = './recommendation-system/final_df'
	else: 
		path = './final_df'

	final_df = pd.read_csv(path)
=======
	knn_model = pickle.load(open(knn_model_path, 'rb'))
	return knn_model

def load_final_df_locally():
	final_df = pd.read_csv(final_df_path)
>>>>>>> recommender-system-2.0
	final_df.set_index('movieId', inplace=True)
	return final_df
