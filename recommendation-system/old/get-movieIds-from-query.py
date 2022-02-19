import sys, json
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import json
from pathlib import Path
import os
import pymongo
import loader


query = sys.argv[1]

uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['finding-movies-to-watch']



#Input: search query, number of movies to return
#Output: array of movieIds
#Takes in a query string, looks up the dataset and returns all the records whose movie titles are a superset of the query
def get_movies_containing_query(query):

	# movies_df = get_movies_from_db()

	movies_df = loader.load_movies_locally()
	
	#Load dataset in dataframe with columns "title" and movieId
	movies_df = movies_df[['title', 'movieId']]

	#Find a subset of movies which contain the query as a substring

	filter = movies_df['title'].str.contains(query)

	#list of movies which contain movie_name in their name
	movie_list_df = movies_df[filter]

	movie_ids = movie_list_df['movieId']

	#convert np array into regular array
	movie_ids_array = movie_ids.values.tolist()


	return movie_list_df



#Given a list of movie titles, we are interested in finding the one which is the most similar to the query string
#Input  -> dataframe with columns ["title","movieId"], and the user query string
#Output -> the movieId (type int) of the movie with the most similar title to the query string
def find_most_similar_movieIds(query, movie_titles_and_ids, n):
	#apply similarity function
	movie_titles_and_ids['similarity_to_query'] = movie_titles_and_ids['title'].apply(lambda x: get_similarity(x, query))	
	# print(movie_titles_and_ids)

	#get movie_id corresponding to max similarity value
	max_similarity = movie_titles_and_ids['similarity_to_query'].max()

	#use panda's idxmax function to get the row corresponding to the max value in a given column.
	max_similarity_idx = movie_titles_and_ids['similarity_to_query'].idxmax()
	most_similar_movie_row = movie_titles_and_ids.loc[[max_similarity_idx]]
	# print(most_similar_movie_row)

	primaryId = most_similar_movie_row['movieId'].values[0]

	#remove primaryId from movie_titles_and_ids, so we don't have duplicates in our JSON object
	movie_titles_and_ids = movie_titles_and_ids[movie_titles_and_ids['movieId'] != primaryId]

	ordered_similarities = movie_titles_and_ids.sort_values(by=['similarity_to_query'], ascending=False)
	others = ordered_similarities['movieId'].values[:n-1]

	#convert from ndarray to list
	others = others.tolist()

	#drop similarity columm
	movie_titles_and_ids.drop(columns=['similarity_to_query'], inplace=True)

	return primaryId, others

def get_similarity(string1, string2):
	return SequenceMatcher(None, string1, string2).ratio()


#Prepare JSON 
#Input  -> movieId of most similar movie, dataframe containing all movie_titles_and_ids which match user query
#Output -> JSON object with format {most_similar: 123, others: [1,2,3,4,...]}
def prepareJSONResponse(n):
	response = {}	

	movie_titles_and_ids = get_movies_containing_query(query) 

	if (movie_titles_and_ids.size == 0):
		response = json.dumps({})
		print(response)	
	else:
		primaryId, others = find_most_similar_movieIds(query, movie_titles_and_ids, n=10)

		data = {"primaryId": int(primaryId), "others": others}

		response = json.dumps(data)

		print(response)


prepareJSONResponse(n=10)

sys.stdout.flush()
	



