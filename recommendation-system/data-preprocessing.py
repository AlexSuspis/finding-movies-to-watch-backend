import pymongo
import pandas as pd
import random
import json




dataset = pd.read_csv('./input/small_dataset/movies.csv')

# print(dataset.columns)
print(dataset)

countries = [
	'Portugal',
	'United Kingdom',
	'United States',
	'France',
	'Brazil',
	'China',
	'India',
]

providers = [
	'Netflix',
	'HBO Max',
	'Amazon Video',
	'Youtube'
]

def get_random_countries():
	global countries
	#print(countries)

	#get random number of random countries
		#choose random number
	r = random.randint(2, len(countries))	

	selected_countries = []
	for i in range(1,r):
		random_country = random.choice(countries)
		if(random_country not in selected_countries):
			selected_countries.append(random_country)

	# print(selected_countries)
	return selected_countries

def get_random_providers():
	global providers
	#print(providers)

	#get random number of random countries
		#choose random number
	r = random.randint(2, len(providers))	

	selected_providers = []
	for i in range(1,r):
		random_provider = random.choice(providers)
		if(random_provider not in selected_providers):
			selected_providers.append(random_provider)

	# print(selected_providers)
	return selected_providers

# get_random_countries()
# get_random_providers()


#1) Preprocess dataset before inserting it into mongo database.

#For each movie entry, add a random number of randomly selected countriesFor each movie entry, add a random number of randomly selected countries
random_countries_list = []
#create a set of random countries for each row in dataset
for i in range(dataset.index.size):
	random_countries_list.append(get_random_countries())

dataset['countries'] = random_countries_list

#For each movie entry, add a random number of randomly selected countriesFor each movie entry, add a random number of randomly selected countries
#create a set of random countries for each row in dataset
random_providers_list = []
for i in range(dataset.index.size):
	random_providers_list.append(get_random_providers())


dataset['providers'] = random_providers_list

# print(dataset.head())
#dataset.set_index('movieId', inplace=True)
# print(dataset.head())





#2) Insert dataset into mongo database. How am I going to do this?
uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)

db = client['finding-movies-to-watch']

#make movies column an index
db.movies.create_index('movieId')
print(db.movies.index_information())

# db.movies.delete_many({})
# print('all movie records in movie collection deleted')

# db.movies.insert_many(dataset.to_dict('records'))
# print("inserted movies from dataset into movie collection")




