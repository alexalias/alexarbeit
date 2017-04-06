import duration_dict
from collections import defaultdict
from statistics import *

# Creates a dictionary of phonemes, which incorporates the duration-dictionary for each phoneme and adds stats
# A much too complicated way of building the dictionary of phonemes out of a dictionary of durations.

# List of phonemes to search for
phoneme_list = ["OY", "aU", "aI"]
# Get the dictionary of lengths
dict_of_lengths = duration_dict.phon_dict(phoneme_list)


# Returns a list of phoneme duration occurencies (duration_list_per_phoneme) 
# 	and a list containing the values of all keys (duration_flat_list).
# Source: already existent dictionary.
def create_list_of_durations():
	# Initialize variables
	duration_list_per_phoneme = []
	value_list = []
	duration_flat_list = []

	# Populate list with keys from duration dictionary
	key_list = dict_of_lengths.keys()

	# Iterate over the keys of the dictionary to get the value lists
	for item in key_list:
		value_list.extend(dict_of_lengths[item])	# Get value list of a specific key
		number_of_key_occurences = int(len(value_list) / 7)		# Divide value list by number of different element-
																# types (attributes) = no. of occurences of a specific duration
		duration_list_per_phoneme.extend([item] * number_of_key_occurences) # list of all duration value occurencies
		#duration_flat_list.append(item)
		duration_flat_list.extend(value_list)
		value_list.clear()  # Reset list, for new key-value pair
	return duration_list_per_phoneme, duration_flat_list
duration_list_per_phoneme, duration_flat_list = create_list_of_durations()


# Writes speech rates to a text file, one column
def write_speech_rate():
	sp_file = open("C:/Users/alexutza_a/Abschlussarbeit/Datenanalyse_Verbmobil/SpeechRate_Histogram.txt", "w")
	#sr_l=duration_flat_list[6::7]
	for elem in duration_flat_list[6::7]:
		sp_file.write(str(round(float(elem), 2)) + "\n")
	sp_file.close()
#write_speech_rate()



# Replaces the speech rate values in the duration_flat_list with normalized values
# Param flat_list = duration_flat_list; sp_list = list of not normalized speech rates; norm_sp_list = list of normalized speech rates
# Return: duration_flat_list with normalized speech rate values
def norm_dur_flat_list(flat_list, sp_list, norm_sp_list):
	for elem in flat_list:
		if elem in sp_list:
					ind = flat_list.index(elem)
					flat_list.remove(elem)
					sp_list.pop(0)
					flat_list.insert(ind, norm_sp_list.pop(0))
	return flat_list
#print(norm_dur_flat_list(duration_flat_list, sp_list, norm_sp_list))

# Returns a dictionary of general duration stats (values) per phoneme (key)
# Stats: Min, Max, Median, Mean, Mode, Standard Deviation, Interval Length
def phoneme_stats(phoneme):
	# Initialize variables
	duration_list = []
	stats_dict = defaultdict(list)
	stat_values = []

	# Populate duration list
	duration_list.extend(create_list_of_durations(phoneme))	

	# Create variables for Mean, Min, Max
	mean_p = mean(duration_list)
	min_duration = min(duration_list)
	max_duration = max(duration_list)
	
	stat_values.extend([min_duration, max_duration, median(duration_list),
		mean_p, mode(duration_list), pstdev(duration_list, mean_p), max_duration-min_duration])
	stats_dict[phoneme].append(dict_of_lengths)
	for value in stat_values:
		stats_dict[phoneme].append(value)
	return stats_dict

#print(phoneme_stats("a"))