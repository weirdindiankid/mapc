# Filename: wit.py
# Author: Dharmesh Tarapore <dharmesh@bu.edu>
# Description: Wit AI quasi wrapper. 
from wit import Wit
import secrets

def get_num_rooms_from_sentence(sentence):
	'''
		Input: Rental listing title.
		Output: Number of bedrooms using the num_bedrooms entity. If 
		        a guess is unavailable, we just return 1 (best guess).
	'''
	try:
		some_abysmally_large_number = 10
		# Initialise wit.ai
		client = Wit(secrets.WIT_AI_CLIENT_ACCESS_TOKEN)
		# Create wit message (returns dict)
		resp_dict = client.message(sentence)
		if 'entities' in resp_dict.keys():
			entities = resp_dict['entities']
			# Now see if num_bedrooms exists
			if 'num_bedrooms' in entities:
				num_bedrooms = entities['num_bedrooms']
				# Some responses contain multiple elements in a list
				bedrooms = []
				for rdict in num_bedrooms:
					bedrooms.append(int(rdict['value']))
				# Sort it
				bedrooms.sort()
				# Next, we see if the max is some abysmally large number
				for i in bedrooms[::-1]:
					if i < some_abysmally_large_number:
						return i
		# In all other instances, return best guess.
		return 1
	except:
		print("Wit AI error.")
		return 1