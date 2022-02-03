import pymongo
import pandas as pd
import random

#Replace <password> with the password for the root_user user. Replace myFirstDatabase with the name of the database that connections will use by default.
uri = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)

db = client.movies

print(db)


dataset = pd.read_csv('./input/small_dataset/movies.csv')

print(dataset.columns)

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

	print(selected_countries)

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

	print(selected_providers)

get_random_countries()
get_random_providers()

#Preprocess dataset before inserting it into mongo database.

#For each movie entry, add a random number of randomly selected countriesFor each movie entry, add a random number of randomly selected countries

#For each movie entry, add a random number of randomly selected countriesFor each movie entry, add a random number of randomly selected countries