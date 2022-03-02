import loader
import utils
import json
import sys

def find_movieIds_from_closest_titles_to(query, n):
	movies_df = loader.load_processed_movies_locally()
	# print(movies_df['title'])
	# print(movies_df['clean_title'])

	clean_query = utils.clean_string(query)
	# print(clean_query)

	movies_df['similarity_to_query'] = movies_df['clean_title'].apply(lambda clean_title: utils.get_string_similarity(clean_title, clean_query))
	# print(movies_df['similarity_to_query'])

	#sort
	movies_df.sort_values(by='similarity_to_query', ascending=False, axis=0, inplace=True)


	#no matches found
	if movies_df['similarity_to_query'].iloc[0] < 0.7:
		print([])
	else:
		top_movieIds = movies_df['movieId'][:n].values
		# utils.get_movie_titles_from_ids(top_movieIds)
		# results = top_movieIds.tolist()
		# print(results)

		print(json.dumps(top_movieIds.tolist()))



# result = find_movieIds_from_closest_titles_to('iron man', 5)
# print(result)

query = str(sys.argv[1])
find_movieIds_from_closest_titles_to(query, 3)
