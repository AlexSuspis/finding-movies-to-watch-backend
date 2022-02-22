from query_search_tasks import find_movieIds_from_closest_titles_to
import sys
import loader
import json
import numpy as np
import utils


query = sys.argv[1]
print(query)
n_total = 20
n_matches = 5
n_recommendations = n_total - n_matches


movieIds = find_movieIds_from_closest_titles_to(query, n_matches)
if len(movieIds) == 0:
	print(json.dumps([]))
else:
	print(movieIds)

	similarity_matrix = loader.load_similarity_matrix_locally()
	print(similarity_matrix)

	top_movieId = movieIds[0]

	row = similarity_matrix[movieIds[0]]
	print(row)

	#find indices of top 10 highest values in row
	#Inspired by: https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array
	recommended_movieIds = np.argpartition(row, -n_recommendations)[-n_recommendations:]
	# utils.get_movie_titles_from_ids(recommended_movieIds)

	print(json.dumps(str(list(recommended_movieIds))))



utils.get_movie_titles_from_ids(movieIds)