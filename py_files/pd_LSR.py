import os
import glob
import re
import numpy as np
from collections import defaultdict
import speech_rate

# Returns a dictionary of phoneme occurences (keys) in the training data and their durations (values), and LSR (values)
# Looks like {a: [1452, 0.8, 799, 0.5], b : [655, 0.5, 799, 0.45]...}
def read_trainig_files():
	training_dict = defaultdict(list)
	os.chdir("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training")
	
	#Iterate over the training files
	for file in glob.glob("*.par"):
		work_file = open(file)

		for line in work_file:
			if re.match("MAU", line):
				training_dict[line.split()[4]].append(int(line.split()[2]))
				word_duration, phon_count, syl_count = speech_rate.word_duration(file, int(line.split()[3]))
				training_dict[line.split()[4]].append((word_duration/0.0000625)/phon_count)
				#training_dict[line.split()[4]].append(speech_rate.local_speech_rate(file, int(line.split()[3])))

		work_file.close()
	
	# Remove breaks from the data
	x = training_dict.pop("<p:>")

	return training_dict

# A dictionary giving the values of Mean and SD in a list for each encountered phoneme.
def phone_stats(training_dict):
	stat_dict = defaultdict(list)

	for phoneme in training_dict.keys():
		stat_dict[phoneme].append(int(round(np.mean(training_dict[phoneme][::2]), 0)))
		stat_dict[phoneme].append(int(round(np.std(training_dict[phoneme][::2]), 0)))

	return stat_dict

# Not used
def mean_of_means(stat_dict):
	m1 = 0

	for p in stat_dict:
		m1 += stat_dict[p][0]
	mom = m1 / len(stat_dict.keys())
	return mom 

# Returns a list of phoneme occuring in the test files, followed by their respective durations
# Looks like: ["a", 583, 0.5, "b", 12, 0.78, "a", 489, 0.12, ...]
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
				word_duration, phon_count, syl_count = speech_rate.word_duration(file, int(line.split()[3]))
				compare_list.append(round((word_duration/0.0000625)/phon_count, 1)) # speech rate as word_duration / # phonemes
				#compare_list.append(speech_rate.local_speech_rate(file, int(line.split()[3])))
		work_file.close()
	#print(compare_list)
	# Remove breaks from the data

	# Get list of indexes for occurences of <p:>
	pause_index = [i for i, val in enumerate(compare_list) if val == "<p:>"]
	#print(len(pause_index))
	pause_dur = [i + 1  for i in pause_index]
	pause_stat = [j + 1  for j in pause_dur]
	p_l = [x for y in zip (pause_index, pause_dur) for x in y]
	p_list = p_l + pause_stat
	#print(len(p_list))
	actual_list = []

	#print(compare_list)
	ind = 0
	# Copy list to new list, without pauses
	for el in compare_list:
		if ind not in p_list:
			actual_list.append(el)
		ind += 1

	return actual_list

# Returns a dictionary of the official phoneme means for VM1+2
def official_stats():
	o_dict = defaultdict(list)
	#omedian_dict = defaultdict(float)
	official_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training/Basic_german_phone_list.txt")
	for line in official_file:
		if len(line.split()[0]) < 3:
			o_dict[line.split()[0]].append(int(round((float(line.split()[6])/0.0000625), 0)))
			o_dict[line.split()[0]].append(int(round((float(line.split()[7])/0.0000625), 0)))
			#omedian_dict[line.split()[0]] = int(round((float(line.split()[9])/0.0000625), 0))
	#print(o_dict)
	return o_dict#, omedian_dict

# Quote of phoneme mean duration being greater than the local speech rate (as word duration / no. of phonemes)
def test_mean(training_dict, stat_dict):
	test_dict = defaultdict(float)

	for elem in training_dict.keys():
		rate_list = training_dict[elem][1::2]
		test_mean_list = [ 1 for x in rate_list if x <= stat_dict[elem][0]]
		test_dict[elem] = len(test_mean_list)/len(rate_list)
	return test_dict

# Create a list of durations and a list of word durations from the training data
def dur_vs_rate(training_dict):
    duration_list = []
    rate_list = []
    for el in training_dict.keys():
        duration_list += training_dict[el][::2]
        rate_list += training_dict[el][1::2]
    return duration_list, rate_list
#duration_list, rate_list = dur_vs_rate(read_trainig_files())

# Returns a list with predicted durations for the phonemes of the test set.
# Predicted durations come from the observed durations in the training set (mean and SD), and
#  from the official mean statistics of Verbmobil, for phonemes, which don't occur in the training set.
# @param testfile_list: the list returned by read_testfiles()
#	Looks like: ["a", 583, 0.5, "b", 12, 0.78, "a", 489, 0.12, ...]
# @param stat_dict: dictionary giving the mean and the SD for each phoneme 
#   NO: the full dictionary built from the training data
#	NO: Looks like {a: [1452, 0.8, 799, 0.5], b : [655, 0.5, 799, 0.45]...}
def create_prediction_list(testfile_list, stat_dict):
	phone_list = testfile_list[::3]
	vowels = ["a:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "a~:", "a", "e", "E", "i", "o", "u", "y", "2", "a~", "@", "9"]
	#print(phone_list)
	#mini = min(testfile_list[1::3])
	#lsr_list = testfile_list[2::3]
	prediction_list = []
	#off_dict = official_stats()

	#print(len(lsr_list))
	#print(len(phone_list))
	#print(phone_list)
	#prediction_list = [ training_dict.get(el, o_dict[el]) for el in phone_list ]
	#prediction_list = [ training_dict.get(el, omedian_dict[el]) for el in phone_list ]
	i = 0
	for phone in phone_list:
		#print(i)
		#print(phone)
	#	prediction_list = testfile_list[2::3]
		if phone in stat_dict.keys():
	#		prediction_list.append(mini + (stat_dict[phone][0]-mini)*lsr_list[i]) # Klatt
	#		prediction_list.append(mini + stat_dict[phone][1]*lsr_list[i])  # Klatt mit SD statt Differenz
	#		prediction_list.append(mini + stat_dict[phone][1]/3*lsr_list[i])  # Klatt mit SD / 3
	#		prediction_list.append(stat_dict[phone][0]) # just mean per phoneme
	#		if lsr_list[i] <= 0.45:
	#			prediction_list.append(stat_dict[phone][0] - stat_dict[phone][1]/3) # mean +/- sigma/3 
	#		elif lsr_list[i] >= 0.65:
	#			prediction_list.append(stat_dict[phone][0] + stat_dict[phone][1]/3)
	#		else:
	#			prediction_list.append(stat_dict[phone][0])
			if phone in vowels:						# split for using SR instead of mean
				if test_mean(read_trainig_files(), stat_dict)[phone] >= 0.8:		
					prediction_list.append(testfile_list[i*3+2] + ((stat_dict[phone][1]/3)))
				elif test_mean(read_trainig_files(), stat_dict)[phone] <= 0.45:
					prediction_list.append(testfile_list[i*3+2] - ((stat_dict[phone][1]/3)))
				else: 
					prediction_list.append(testfile_list[i*3+2])
			else:
				prediction_list.append(stat_dict[phone][0])
	#	else:
	#		prediction_list.append(mini + (off_dict[phone][0]-mini)*lsr_list[i]) # Klatt mit offiziellen Werten
	#		prediction_list.append(mini + off_dict[phone][1]*lsr_list[i])  # Klatt mit SD statt Differenz
	#		prediction_list.append(mini + off_dict[phone][1]/3*lsr_list[i]) 	# # Klatt mit SD / 3
	#		prediction_list.append(off_dict[phone][0])  # mean / phoneme (aus offiziellen Werten)
	#		
	#		if lsr_list[i] <= 0.45:
	#			prediction_list.append(off_dict[phone][0] - (off_dict[phone][1]/3))
	#		elif lsr_list[i] >= 0.65:
	#			prediction_list.append(off_dict[phone][0] + (off_dict[phone][1]/3))
	#		else:
	#			prediction_list.append(off_dict[phone][0])
		i += 1

	return prediction_list