import os
import glob
import re
import numpy as np
from collections import defaultdict

# Returns a dictionary of the official phoneme means for VM1+2
def standard_value_means():
	o_dict = defaultdict(float)
	omedian_dict = defaultdict(float)
	official_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training/Basic_german_phone_list.txt")
	for line in official_file:
		if len(line.split()[0]) < 3:
			o_dict[line.split()[0]] = int(round((float(line.split()[6])/0.0000625), 0))
			omedian_dict[line.split()[0]] = int(round((float(line.split()[9])/0.0000625), 0))
	#print(o_dict)
	return o_dict, omedian_dict
o_dict, omedian_dict = standard_value_means()

# Returns a dictionary of phoneme occurences (keys) in the training data and their durations (values)
def read_trainig_files():
	training_dict = defaultdict(list)
	os.chdir("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training")
	
	#Iterate over the training files
	for file in glob.glob("*.par"):
		work_file = open(file)

		for line in work_file:
			if re.match("MAU", line):
				training_dict[line.split()[4]].append(int(line.split()[2]))
		work_file.close()
	
	# Remove breaks from the data
	x = training_dict.pop("<p:>")

	return training_dict

# Returns a list of phoneme occuring in the test files, followed by their respective durations
# Looks like: ["a", 583, "b", 12, "a", 489, ...]
def read_testfiles():
	compare_list = []
	os.chdir("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test")

	#Iterate over the test files
	for file in glob.glob("*.par"):
		work_file = open(file)

		for line in work_file:
			if re.match("MAU", line):
				compare_list.append(str(line.split()[4]))
				compare_list.append(int(line.split()[2]))
		work_file.close()
	
	# Remove breaks from the data

	# Get list of indexes for occurences of <p:>
	pause_index = [i for i, val in enumerate(compare_list) if val == "<p:>"]
	#print(pause_index)
	pause_dur = [i + 1 for i in pause_index]
	p_list = [x for y in zip (pause_index, pause_dur) for x in y]
	#print(p_list)
	actual_list = []

	#print(compare_list)
	ind = 0
	# Copy list to new list, without pauses
	for el in compare_list:
		if ind not in p_list:
			actual_list.append(el)
		ind += 1

	return actual_list

# Calculates the mean of phoneme durations / phoneme and puts it at the beginning of the value lists
# Returns:
# - the phoneme dict of the training data updated with the mean duration of each phoneme 
# 	at the beginning of each value list
# - a separate dict of encountered phonemes and their mean
def calculate_pho_mean(phon_dict):
	test_dict = defaultdict(int)
	tm_dict = defaultdict(int)
	for key in phon_dict.keys():
		key_mean = np.mean(phon_dict[key])
		key_median = np.median(phon_dict[key])
		phon_dict[key].insert(0, int(round((key_mean), 0)))
		test_dict[key] = int(round((key_mean)))
		tm_dict[key] = int(round((key_median)))
	#print(phon_dict)
	return phon_dict, test_dict, tm_dict

phon_dict, test_dict, tm_dict = calculate_pho_mean(read_trainig_files())

# Returns a list with predicted durations for the phonemes of the test set.
# Predicted durations come from the observed durations in the training set (mean), and
#  from the official mean statistics of Verbmobil, for phonemes, which don't occur in the training set.
def create_prediction_list(testfile_list, training_dict):
	phone_list = testfile_list[::2]
	#print(phone_list)
	#prediction_list = [ training_dict.get(el, o_dict[el]) for el in phone_list ]
	prediction_list = [ training_dict.get(el, omedian_dict[el]) for el in phone_list ]
	return prediction_list

#print(create_prediction_list(read_testfiles(), test_dict))
#print(read_testfiles())