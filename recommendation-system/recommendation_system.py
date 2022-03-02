import sys
import loader
import json
import numpy as np
import utils



def get_recommendations_for_movieId(movieId, n_recommendations):
	similarity_matrix = loader.load_similarity_matrix_locally()
	# print(similarity_matrix)

	row = similarity_matrix[movieId]
	# print(row)
	sorted_row = row.sort_values(ascending=False)
	# print(sorted_row)
	recommended_movieIds = sorted_row[:n_recommendations].index
	# print(recommended_movieIds)

	#find indices of top 10 highest values in row
	#Inspired by: https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array
	# idx_recommended_movieIds = np.argpartition(row, -n_recommendations)[-n_recommendations:]

	# utils.get_movie_titles_from_ids(recommended_movieIds)

	result = json.dumps(recommended_movieIds.tolist())
	print(result)


movieId = int(sys.argv[1])
get_recommendations_for_movieId(movieId, 15)

# n_total = 20
# n_matches = 5
# n_recommendations = n_total - n_matches
