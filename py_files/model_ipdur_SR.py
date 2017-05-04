import numpy as np
from collections import defaultdict
import model_utilities
import model_ipdur
import new_SR

# This is a relatively static phoneme duration prediction model which only considers the median (or mean) value of a specific phoneme
# and one split of speech rate values.
#
# Predicted value = median or mean of phon_dur in provided (training) dataset

###################################################### START ##################################################################

############## STATIC DATA STRUCTURES (not dataset specific) ##################################


# Create list of filepaths to explore. This one uses entire data set, for exploration purposes.
# path_list_training = verbmo_par_files('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par')
path_list_training = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training_a')

valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
                 "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
                 "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

vowel_list = ["Q", "a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "@", "6", "a:", "a~:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "OY", "aU", "aI"]

#################################### DYNAMIC DATA STRUCTURES (training data) ################################

# Returns: (type: int) the predicted duration (samples) of given phoneme based on number of phonemes in word
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
def pdur_prediction_value(datei, word_no, phoneme, model):
	pdur_compressed_dict = model_ipdur.phon_dur_compressed_dict(model_utilities.phon_dur_dict(path_list_training))
	word_dur, phoneme_count, mau_syl_count = model_utilities.word_statistics(datei, word_no)
	SR = new_SR.get_word_SR(datei, word_no)[0]
	SD = 73.91
	#print(pdur_compressed_dict)
	if SR >= 75:
		try:
			pdur_prediction = int(round(pdur_compressed_dict[phoneme][model], 0)) + int(round(SD/3, 0))
		except:
			pdur_prediction = int(round(word_dur / phoneme_count, 0))
	else:
		try:
			pdur_prediction = int(round(pdur_compressed_dict[phoneme][model], 0)) - int(round(SD/3, 0))
		except:
			pdur_prediction = int(round(word_dur / phoneme_count, 0))

	return pdur_prediction

#print(pdur_prediction_value("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par", 10, "t", 0))