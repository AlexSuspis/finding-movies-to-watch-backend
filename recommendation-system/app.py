import sys, json
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import json


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
#Input  -> dataframe with columns ["title","movieId"], and the user query string
#Output -> the movieId (type int) of the movie with the most similar title to the query string
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

	#drop similarity columm
	movie_titles_and_ids.drop(columns=['similarity_to_query'], inplace=True)

	return most_similar_movieId

def get_similarity(string1, string2):
	return SequenceMatcher(None, string1, string2).ratio()



#From the user query, find list of movie titles and their respective movie_ids containing it.
movie_titles_and_ids = get_movies_containing_query(query,5) 
#print(movie_titles_and_ids)

print()

most_similar_movieId = find_most_similar_movieId(query, movie_titles_and_ids)
#print(most_similar_movieId)


#Prepare JSON 
#Input  -> movieId of most similar movie, dataframe containing all movie_titles_and_ids which match user query
#Output -> JSON object with format {most_similar: 123, others: [1,2,3,4,...]}
def prepareJSONResponse(primaryId, movie_titles_and_ids):
	response = {}	

	#remove primaryId from movie_titles_and_ids, so we don't have duplicates in our JSON object
	movie_titles_and_ids = movie_titles_and_ids[movie_titles_and_ids['movieId'] != primaryId]

	others = movie_titles_and_ids['movieId'].values.tolist()

	# print(others)
	# print(type(others))
	# print()

	data = {"primaryId": int(primaryId), "others": others}
	# print(data)
	# print()	

	jsonResponse = json.dumps(data)
	# print(json.dumps(data))
	# print(jsonResponse)

	return jsonResponse



response = prepareJSONResponse(most_similar_movieId, movie_titles_and_ids)

print(response)
print(type(response))

sys.stdout.flush()


