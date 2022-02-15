import sys
import pandas as pd
import json


movieId = int(sys.argv[1])
#Script input: movieId : int 
#Script output: list of n integers, each one being a recommended movieId (similar to the input movieId)  

#Check if movieId exists in dataset
	#print [] if does not exist
	#else continue
if(movieId == -1):
	print([])
else:
	# print([int(movieId)] * 10)

	#Load recommendation model
	import pickle

	# filename = 'knn_model.sav'
	filename = 'recommendation-system/knn_model.sav'
	knn_model = pickle.load(open(filename, 'rb'))
	# print(knn_model)

	# final_df = pd.read_csv('final_df.csv')
	final_df = pd.read_csv('recommendation-system/final_df.csv')
	final_df.set_index('movieId', inplace=True)
	# print(final_df)
	# print(final_df)
	try:
		movie_row = final_df.loc[movieId]

		distances, indices = knn_model.kneighbors(movie_row.values.reshape(1,-1))
		# print()
		# print('distances: ', distances) 
		# print('indices: ', indices)

		#get movieIds from indices
		movieIds = []
		for idx in indices[0]:
			# print(final_df.iloc[idx])
			movieIds.append(int(final_df.index[idx]))

		#remove initial movieId from movieIds list
		movieIds.remove(movieId)

		# print()
		# print(movieIds)
		# print(type(movieIds))


		response = json.dumps((movieIds))
		print(response)

		#Predict recommended films
			#Get 10 most similar films 
			#Create an array
			#JSON.dump(array)
			#print(array)
		# print(movie_row)

	except:
		print([])
		









