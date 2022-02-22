import loader_saver as io
import utils

def preprocess_movies():

	movies_df = io.load_movies_locally()
	print(movies_df.columns)

	#split genres into a list
	movies_df['genres'] =  movies_df['genres'].apply(lambda x: x.split("|"))
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

	#save locally and to database		
	# io.save_movies_locally(movies_df)
	# io.post_movies_to_db(movies_df)


def preprocess_similarity_matrix():
	pass


preprocess_movies()