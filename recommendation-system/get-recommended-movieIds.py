import sys
import pandas as pd
import json


movieId = int(sys.argv[1])
#Script input: movieId : int 
#Script output: list of n integers, each one being a recommended movieId (similar to the input movieId)  


#if using from the command line
# ratings_df = pd.read_csv('./input/small_dataset/ratings.csv')

#else if called from express server, the path to dataset must be relative to index.js file, not this script! Easy mistake to make
# ratings_df = pd.read_csv('./recommendation-system/input/small_dataset/ratings.csv')

#Does movieId exist in dataset?
#print [] if does not exist
#return
if(movieId == -1):
	print([])
else:
	print([int(movieId)] * 10)


#continue if exists



# print(ratings_df)
# ratings_df.drop(columns=['timestamp'], inplace=True)
# print(ratings_df)




#We are interested in creating a knn model so we can classify movieIds and get the n nearest neighbours
#We must first pre-process the data:
	#outliers in data
	#null/missing values


