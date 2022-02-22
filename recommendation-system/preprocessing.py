import loader
import utils

def preprocess_movies():

	movies_df = loader.load_movies_locally()
	print(movies_df.columns)

	#split genres into a list
	movies_df['genres'] =  movies_df['genres'].apply(lambda x: x.split("|"))
	print(movies_df)

	#clean movie titles
	movies_df['clean_title'] = movies_df['title'].apply(lambda x: utils.clean_string(x))
	print(movies_df)

	#countries


	#providers	


def preprocess_similarity_matrix():
	pass


preprocess_movies()