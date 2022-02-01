import sys, json
import pandas as pd
import numpy as np
from difflib import SequenceMatcher


query = sys.argv[1]

#Input: search query, number of movies to return
#Output: array of movieIds
#Takes in a query string, looks up the dataset and returns the first
	# n movieIds which have this query as a substring in their title.
def get_movies_containing_query(query, n):

	#if using from the command line
	movies_df = pd.read_csv('./input/small_dataset/movies.csv')

	#else if called from express server, the path to dataset must be relative to index.js file, not this script! Easy mistake to make
	#movies_df = pd.read_csv('./recommendation-system/input/small_dataset/movies.csv')
	
	#Load dataset in dataframe with columns "title" and movieId
	movies_df = movies_df[['title', 'movieId']]

	#Find a subset of movies which contain the query as a substring

	filter = movies_df['title'].str.contains(query)

	#list of movies which contain movie_name in their name
	movie_list_df = movies_df[filter]
	#print(movie_list_df)

	movie_ids = movie_list_df['movieId']

	# movie_titles = movie_list_df['title']
	# print(movie_titles)

	#convert np array into regular array
	movie_ids_array = movie_ids.values.tolist()


	return movie_list_df




#Given a list of movie titles, we are interested in finding the one which is the most similar to the query string
#Input  -> dataframe with columns ["title","movieId"]
#Output -> JSON object with format {most_similar: 123, others: [1,2,3,4,...]}
def find_most_similar_movieId(query, movie_titles_and_ids):
	#get list of movie titles from movie_titles_and_ids
	movie_titles = movie_titles_and_ids['title'].tolist()
	#print(movie_titles)

	#apply similarity function
	movie_titles_and_ids['similarity_to_query'] = movie_titles_and_ids['title'].apply(lambda x: get_similarity(x, query))	
	#print(movie_titles_and_ids)

	#get movie_id corresponding to max similarity value
	max_similarity = movie_titles_and_ids['similarity_to_query'].max()

	#use panda's idxmax function to get the row corresponding to the max value in a given column.
	max_similarity_idx = movie_titles_and_ids['similarity_to_query'].idxmax()
	most_similar_movie_row = movie_titles_and_ids.loc[[max_similarity_idx]]
	#print(most_similar_movie_row)
	#print()

	most_similar_movieId = most_similar_movie_row['movieId'].values[0]
	#print(most_similar_movieId)

	return most_similar_movieId

def get_similarity(string1, string2):
	return SequenceMatcher(None, string1, string2).ratio()

#From the user query, find list of movie titles and their respective movie_ids containing it.
movie_titles_and_ids = get_movies_containing_query(query,5) 
#print(movie_titles_and_ids)

print()

most_similar_movieId = find_most_similar_movieId(query, movie_titles_and_ids)


print(most_similar_movieId)
sys.stdout.flush()


