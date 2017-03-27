import numpy as np
from collections import defaultdict
import model_utilities

# This is a phoneme duration prediction model for varying word length ### duration.
# NO NO: It supposes we know the target word duration, and is based only on that feature.
#
# Information from the training data is used to compute the steak each phoneme takes in a n-phoneme-long word.
#
# Predicted value = median or mean of phon_dur in words of length x

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
			phon_wl_compressed_dict[phon][w_leng] = [round(np.median(phon_wordleng_dict[phon][w_leng][1::3]), 3)]
			phon_wl_compressed_dict[phon][w_leng].append(round(np.mean(phon_wordleng_dict[phon][w_leng][1::3]), 3))
			phon_wl_compressed_dict[phon][w_leng].append(round((np.median(phon_wordleng_dict[phon][w_leng][1::3]) + np.mean(phon_wordleng_dict[phon][w_leng][1::3]))/2, 3))
	return phon_wl_compressed_dict

phon_wl_compressed_dict = phon_wl_compressed_dict(model_utilities.phon_wordleng_dict(path_list_training))

###################################### DYNAMIC DATA STRUCTURES (testdata) ##########################################

# Returns: (type: int) the predicted duration (samples) of given phoneme based on number of phonemes in word
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
def pdur_prediction_value(datei, word_no, phoneme, model):
	word_duration, phoneme_count, mau_syl_count = model_utilities.word_statistics(datei, word_no)
	pdur_prediction = int(round(phon_wl_compressed_dict[phoneme][phoneme_count][model], 0))

	return pdur_prediction