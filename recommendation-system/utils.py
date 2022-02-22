import re
import string

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