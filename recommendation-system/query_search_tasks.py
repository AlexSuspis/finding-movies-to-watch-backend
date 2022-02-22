import loader
import utils

def find_movieIds_from_closest_titles_to(query, n):
	movies_df = loader.load_processed_movies_locally()
	# print(movies_df['clean_title'])

	clean_query = utils.clean_string(query)
	# print(clean_query)

	movies_df['similarity_to_query'] = movies_df['clean_title'].apply(lambda clean_title: utils.get_string_similarity(clean_title, clean_query))
	# print(movies_df['similarity_to_query'])

	#sort
	movies_df.sort_values(by='similarity_to_query', ascending=False, axis=0, inplace=True)
	# print(movies_df['similarity_to_query'])

	#no matches found
	if movies_df['similarity_to_query'].iloc[0] < 0.7:
		return []
	else:
		top_movieIds = movies_df['similarity_to_query'][:n].index
		return top_movieIds


# find_movieIds_from_closest_titles_to('spider-maNaasdasdas', 5)