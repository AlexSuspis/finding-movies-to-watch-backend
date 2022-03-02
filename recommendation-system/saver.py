import pymongo
import pandas as pd
import pickle


uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']



def save_preprocessed_movies_locally(movies_df):
	try:
		directory = './processed-data/'
		filename = 'movies_processed.csv'
		movies_df.to_csv(directory+filename, index=False)
		print(f'processed movies dataframe successfully saved in {directory} as: {filename}')

	except:
		print('An error occurred while attempting to save processed movie_df locally') 


def post_preprocessed_movies_to_db(movies_df):
	db.movies.delete_many({})
	print('all movie records in movie collection deleted')

	db.movies.insert_many(movies_df.to_dict('records'))
	print("inserted movies from dataset into movie collection")
	return

def save_similarity_matrix_locally(similarity_matrix):
	try:
		pickle.dump(similarity_matrix, open('./processed-data/similarity_matrix.dat','wb'))
		print('similarity_matrix successfully saved!')
	except:
		print('Something went wrong while attempting to save similarity_matrix')

	pass
