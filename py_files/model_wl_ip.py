import re
import numpy as np
from collections import defaultdict
import model_utilities

# This is a phoneme duration prediction model for varying word duration.
# It supposes we know the target word duration, and is based only on that feature.
#
# Information from the training data is used to compute the steak each phoneme takes in a n-phoneme-long word.
#
# Predicted value = steak*w_dur/class-member-count-in-word

###################################################### START ##################################################################

############## STATIC DATA STRUCTURES (not dataset specific) ##################################


# Create list of filepaths to explore. This one uses entire data set, for exploration purposes.
# path_list_training = verbmo_par_files('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par')
path_list_training = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training')

valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
                 "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
                 "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

#################################### DYNAMIC DATA STRUCTURES (training data) ################################

# Processed version of the phon_wordleng_dict (defined in module model_utilities): 
#    - the value-lists of the inner dict include only the phoneme proportions for the given word length (inner key)
# Returns: a dictionary. Looks like: 
# {"a" : { 1 : [median_a1, mean_a1, (m_a1 + m_a1) /2], 2 : [median_a2, mean_a2, (m_a2 + m_a2) /2], ...}, 
#  "b" : { 1 : [...], ...}, ...}
def phon_wl_compressed_dict(phon_wordleng_dict):
	phon_wl_compressed_dict = dict.fromkeys(phon_wordleng_dict.keys(), defaultdict(list))
	pho_key_list = [key for key, val in phon_wordleng_dict.items()]

	for phon in pho_key_list:
		for w_leng in phon_wordleng_dict[phon].keys():
			phon_wl_compressed_dict[phon][w_leng] = [round(np.median(phon_wordleng_dict[phon][w_leng][2::3]), 3)]
			phon_wl_compressed_dict[phon][w_leng].append(round(np.mean(phon_wordleng_dict[phon][w_leng][2::3]), 3))
			phon_wl_compressed_dict[phon][w_leng].append(round((np.median(phon_wordleng_dict[phon][w_leng][2::3]) + np.mean(phon_wordleng_dict[phon][w_leng][2::3]))/2, 3))
	return phon_wl_compressed_dict

phon_wl_compressed_dict = phon_wl_compressed_dict(model_utilities.phon_wordleng_dict(path_list_training))

###################################### DYNAMIC DATA STRUCTURES (testdata) ##########################################

# Wendet den phon_wl_compressed_dict auf dem vorgegebenen Wort ein
# Return: dictionary mit den entsprechenden phoneme-steaks für das aktuelle Wort (erfasst in composition_dict)
#
# Looks like: phon_wl_compressed_dict but is not nested anymore: {"a" : [median1, mean1, (m1+m2)/2 ], "aU" : [...], ...}
#      and contains as keys only phonemes from the given word (only keys of composition_dict)
def phoneme_steak(composition_dict):
	phoneme_steak_dict = dict.fromkeys(composition_dict.keys())
	for phoneme in composition_dict.keys():
		phoneme_steak_dict[phoneme] = phon_wl_compressed_dict[phoneme][len(composition_dict)]

	return phoneme_steak_dict


# Return: A dictionary of word composition. 
# Looks like:  {"g" : 1, "@" : 1, "n": 1, "aU" : 1}
def build_composition_dict(datei, word_no):
	work_file = open(datei)

	# Initialize composition_dict with value_type : int
	composition_dict = defaultdict(int)

	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == word_no):
			composition_dict[str(line.split()[4])] += 1
	work_file.close()
	return composition_dict
#print(build_composition_dict("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par", 10))


# Returns: (type: int) the predicted duration (samples) of given phoneme based on word composition
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
def pdur_prediction_value(datei, word_no, phoneme, model):
	composition_dict = build_composition_dict(datei, word_no)
	word_dur, phoneme_count, mau_syl_count = model_utilities.word_statistics(datei, word_no)

	# Actually calculate the phon duration prediction
	pdur_prediction = int(round( ((word_dur * phoneme_steak(composition_dict)[phoneme][model])/composition_dict[phoneme]), 0))

	return pdur_prediction
#print(pdur_prediction_value("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test1/g002acn1_000_AAJ.par", 10, "t", 0))