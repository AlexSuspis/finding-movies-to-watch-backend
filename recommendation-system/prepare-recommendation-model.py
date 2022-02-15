import pandas as pd


#LOAD DATASET
#if using from the command line
ratings_df = pd.read_csv('./input/small_dataset/ratings.csv')

#else if called from express server, the path to dataset must be relative to index.js file, not this script! Easy mistake to make
# ratings_df = pd.read_csv('./recommendation-system/input/small_dataset/ratings.csv')
# print(ratings_df)

ratings_df.drop(columns=['timestamp'], inplace=True)
print(ratings_df)


#We must first pre-process the data:

#Get a dataframe with movieIds as index, and userIds as each column. Values are 
final_df = ratings_df.pivot(index = 'movieId', columns='userId', values='rating')

#1) Null/missing values	
final_df.fillna(0, inplace=True)
# print(final_df)

#Count number of ratings each movie got
no_ratings_per_movie = ratings_df.groupby('movieId')['rating'].agg('count')
# print(no_ratings_per_movie)

#2) Discard movies with too few user ratings
filter_movies_with_low_amount_ratings = no_ratings_per_movie > 50

final_df = final_df.loc[filter_movies_with_low_amount_ratings,:]
#3) Discard users with too few rated movies

#Count number of movies each user rated
no_movies_rated_per_user = ratings_df.groupby('userId')['rating'].agg('count')
# print(no_movies_rated_per_user)

filter_users_with_low_amount_ratings = no_movies_rated_per_user > 50
# print(filter_users_with_low_amount_ratings)

final_df = final_df.loc[:,filter_users_with_low_amount_ratings]
print(final_df)




#We are interested in creating a knn model so we can classify movieIds and get the n nearest neighbours
from sklearn.neighbors import NearestNeighbors
import pickle
knn_model = NearestNeighbors(n_neighbors=11, algorithm='ball_tree')
knn_model.fit(final_df)
print(knn_model)

#save knn model with pickle
#https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
filename = 'knn_model.sav'
pickle.dump(knn_model, open(filename, 'wb'))
print('knn_model saved to current directory!')

#save final_df with pickle
#https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
filename = 'final_df.csv'

# pickle.dump(final_df.to_csv, open(filename, 'wb'))
final_df.to_csv('final_df.csv')
print('final_df saved to current directory!')





