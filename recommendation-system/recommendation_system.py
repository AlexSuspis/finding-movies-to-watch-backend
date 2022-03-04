import sys
import loader
import json
import numpy as np
import utils

def predict_similairity_matrix(movieId, n_recommendations):
	similarity_matrix = loader.load_similarity_matrix_locally()
	# print(similarity_matrix)

	row = similarity_matrix[movieId]
	# print(row)
	sorted_row = row.sort_values(ascending=False)
	# print(sorted_row)
	recommended_movieIds = sorted_row[:n_recommendations].index
	# print(recommended_movieIds)

	result = json.dumps(recommended_movieIds.tolist())
	print(result)


movieId = int(sys.argv[1])
predict_similarity_matrix(movieId, 15)

# n_total = 20
# n_matches = 5
# n_recommendations = n_total - n_matches
