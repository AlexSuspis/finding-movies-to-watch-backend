import sys
import pandas as pd
import json
import loader
import time


movieId = int(sys.argv[1])

measure_runtime = False 
if (measure_runtime):
	startTime = time.time()

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

	knn_model = loader.load_knn_model_locally() 
	final_df = loader.load_final_df_locally()
	
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
		


if(measure_runtime):
	totalTime = time.time() - startTime
	print('script run time: {totalTime: .2f} for movieId {movieId}'.format(totalTime=totalTime, movieId=movieId))









