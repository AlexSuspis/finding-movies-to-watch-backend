import pymongo
import pandas as pd
import pickle



uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']

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

def get_ratings_from_db():
	ratings = db.original_ratings.find()
	ratings_df = pd.DataFrame(ratings).drop(columns=['_id'])
	return ratings_df

def load_knn_model_locally():
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
	final_df.set_index('movieId', inplace=True)
	return final_df
