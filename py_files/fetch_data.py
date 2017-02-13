import os
import glob
import re
import numpy as np
from collections import defaultdict

# Returns a dictionary of the official phoneme means for VM1+2
def standard_value_means():
	o_dict = defaultdict(float)
	official_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training/Basic_german_phone_list.txt")
	for line in official_file:
		if len(line.split()[0]) < 3:
			o_dict[line.split()[0]] = int(round((float(line.split()[6])/0.0000625), 0))

	#print(o_dict)
	return o_dict

# Returns a dictionary of phoneme occurences (keys) in the training data and their durations (values)
def read_trainig_files():
	t_dict = defaultdict(list)
	os.chdir("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training")
	
	#Iterate over the training files
	for file in glob.glob("*.par"):
		work_file = open(file)

		for line in work_file:
			if re.match("MAU", line):
				t_dict[line.split()[4]].append(int(line.split()[2]))
		work_file.close()
	
	# Remove breaks from the data
	x = t_dict.pop("<p:>")

	return t_dict

# Calculates the mean of phoneme durations / phoneme and puts it at the beginning of the value lists
# Returns the phoneme dict of the training data updated with the mean duration of each phoneme 
# 	at the beginning of each value list
def calculate_pho_mean(phon_dict):
	for key in phon_dict.keys():
		key_mean = np.mean(phon_dict[key])
		phon_dict[key].insert(0, int(round((key_mean), 0)))
	#print(phon_dict)
	return phon_dict

calculate_pho_mean(read_trainig_files())