import re
import string
import random
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz

def clean_string(s):
	#Lowercase string
	s = s.lower()

	#Remove all spaces
	s = s.replace(' ', '')

	#Inspired by: https://bart.degoe.de/building-a-full-text-search-engine-150-lines-of-code/
	PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))
	s = PUNCTUATION.sub('', s)
	# print(s)
	return s
	
# clean_string("Hello: World!!!!")

def get_string_similarity(string1, string2):
	return SequenceMatcher(None, string1, string2).ratio()



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