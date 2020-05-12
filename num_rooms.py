# Filename: num_rooms.py
# Author: Dharmesh Tarapore <dharmesh@cs.bu.edu>
# Description: This file takes in a spreadsheet as a command line
#              argument and then adds a new column to it. The new 
#              column contains an estimate of the number of rooms
#              for each row that contains a classified ad listing.
#              The algorithm used to estimate the number of rooms
#              and the expected format of the spreadsheet are detailed
#              below.

import pandas as pd
import spacy
import string
import argparse
import sys
from constants import *

#
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.lang.en import English

def add_bu_num_rooms_to_df(input_df):
	'''
		Input: Pandas DataFrame containing a list of all rentals
		Output: A new Pandas DataFrame containing a column with BU's estimate of
		the number of rooms
		Assumptions: Spreadsheets must follow the format outlined in
		full_listings_misclassified_2018.xlsx
	'''
	try:
		# Pragma Mark: NLP Stuff
		# Caveat: this algorithm does not work well, if at all.
		# My goal here has been to setup a pipeline that allows
		# us to estimate the number of rooms, given a row the represents
		# rental listings. We will work on improving this algorithm 2
		# weeks from today (7th May, 2020)
		punctuations = string.punctuation
		# Create our list of stopwords
		# Load English tokenizer, with stopwords
		parser = English()
		stop_words = spacy.lang.en.stop_words.STOP_WORDS
		# FOR POS TAGGING
		#nlp = spacy.load('en')

		num_rooms_global = []; idx_matches = []; correct_rooms = []
		num_rooms_bu = []

		for x in input_df.itertuples():
			title = (x.title); idx = x.Index
			title = nlp(title)
			mapc_numRooms = x.numRooms
			# only looking at rooms_avail
			rooms_avail = x.bedrooms
			dep_tagged = [(word.dep_) for word in title] 
			num_count = dep_tagged.count('nummod') + dep_tagged.count('nmod')
			num_rooms_bu.append(num_count)

		# Pragma Mark: End NLP Stuff
		num_rooms_mapc = list(input_df['numRooms'].values)
		input_df.insert(5, 'numRooms_BU', num_rooms_bu)
		#input_df['numRooms_BU'] = num_rooms_bu
		return input_df
	except Exception as e:
		exit("There was an error processing the numRooms column: " + str(e))

def get_error_rate(input_df):
	'''
	Output: Scalar quantity that counts the number of rooms where BU's calculations
			don't match MAPC's.
	Input:  Pandas DataFrame object containing the numRooms and numRooms_BU columns.
	'''
	error_count = 0
	num_rooms = input_df['numRooms']
	num_rooms_bu = input_df['numRooms_BU']
	for i in range(len(num_rooms)):
		if num_rooms[i] != num_rooms_bu[i]:
			error_count += 1
	return error_count

def get_keywords(spreadsheet):
	'''
	Output: A list containing all possibly keywords that are relevant to classifying 
	        the number of numbers given a listing.

	'''
	# TODO: Clean this up by making this function more generic
	# For now, we note that we are parsing a sheet from the flagged
	# spreadsheet and replacing extraneous strings.
	list_of_keywords = []
	df = pd.read_excel(spreadsheet, sheet_name='keywords')
	list_of_keywords.append(list(df['roomrent'].values))
	for i in list(df['sublet'].values[:3]):
		list_of_keywords.append(i.replace("[two through nine]", ""))
	for i in list(df['shortterm'].values[:1]):
		list_of_keywords.append(i.replace("[two through nine]", ""))
	for i in list(df['shared'].values[:3]):
		list_of_keywords.append(i.replace("[two through nine]", ""))
	return list_of_keywords


def eval_num_rooms(spreadsheet):
	try:
		# Let us read the spreadsheet in
		df = pd.read_excel(spreadsheet, sheet_name='Flagging_misclassifications')
		# Next let us compile a list of pertinent keywords
		keywords = get_keywords(spreadsheet)

		df = add_bu_num_rooms_to_df(df)
		error_count = get_error_rate(df)
		with open('data/error_count.txt', 'w') as f:
			f.write(str(error_count) + '\n')
			f.close()
		df.to_excel('data/estim.xlsx', index=False)
		# Everything succeeded.
		return SUCCESS
		#print(df.columns)
	except Exception as e:
		exit("There was en error reading the spreadsheet in: " + str(e))


if __name__ == "__main__":
	# TODO: Add argparse
	#parser = argparse.ArgumentParser(description='Estimates number of rooms, given a rental listing spreadsheet.')

	# Hardcoded for now. Migrate to using command line args later.
	if len(sys.argv) <= 1:
		print("Please provider a path to an Excel spreadsheet containing rental listings.")
	else:
		spreadsheet = sys.argv[1]
		result = eval_num_rooms(spreadsheet)
		if result == SUCCESS:
			print("Done. Your files are in ./data/")
		else:
			print("An error occurred. eval_num_rooms exited with code: " + str(result))