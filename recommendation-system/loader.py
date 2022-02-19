import pymongo
import pandas as pd
import pickle



#Insert dataset into mongo database. How am I going to do this?
uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']


def get_movies_from_db():
	movies = db.original_movies.find()
	movies_df = pd.DataFrame(movies).drop(columns=['_id'])

	return movies_df

def load_movies_locally():
	movies_df = pd.read_csv('./input/small_dataset/movies.csv')
	# print(dataset.columns)
	# print(dataset)

	return movies_df


#Load Dataset
def load_ratings_locally():

	#if using from the command line
	ratings_df = pd.read_csv('./input/small_dataset/ratings.csv')

	#else if called from express server, the path to dataset must be relative to index.js file, not this script! Easy mistake to make
	# ratings_df = pd.read_csv('./recommendation-system/input/small_dataset/ratings.csv')
	# print(ratings_df)

	ratings_df.drop(columns=['timestamp'], inplace=True)
	# print(ratings_df)
	return ratings_df


def get_ratings_from_db():
	ratings = db.original_ratings.find()
	ratings_df = pd.DataFrame(ratings).drop(columns=['_id'])
	return ratings_df

def load_knn_model_locally():
	filename = './recommendation-models/knn_model.sav'
	# filename = 'recommendation-system/knn_model.sav'
	knn_model = pickle.load(open(filename, 'rb'))
	# print(knn_model)	
	return knn_model
