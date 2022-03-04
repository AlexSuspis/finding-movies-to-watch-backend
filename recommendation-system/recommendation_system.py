import sys
import loader
import json
import numpy as np
import utils

def predict_similarity_matrix(matched_movieIds):
	similarity_matrix = loader.load_similarity_matrix_locally()

	movieId = matched_movieIds[0]

	row = similarity_matrix[movieId]

	#remove records in matched_movieIds, so we don't get recommendation results which have already been found in the search task
	filtered_row = row[~row.index.isin(matched_movieIds)]

	sorted_row = filtered_row.sort_values(ascending=False)
	# print(sorted_row)
	recommended_movieIds = sorted_row[:24-len(matched_movieIds)].index

	# utils.get_movie_titles_from_ids(recommended_movieIds)

	result = json.dumps(recommended_movieIds.tolist())
	print(result)


matched_movieIds = json.loads(sys.argv[1])

predict_similarity_matrix(matched_movieIds)
