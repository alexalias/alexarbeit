import numpy as np
from collections import defaultdict
import model_utilities

# This is a relatively static phoneme duration prediction model which only considers the median (or mean) value of a specific phoneme
#
# Predicted value = median or mean of phon_dur in provided (training) dataset

###################################################### START ##################################################################

############## STATIC DATA STRUCTURES (not dataset specific) ##################################


# Create list of filepaths to explore. This one uses entire data set, for exploration purposes.
# path_list_training = verbmo_par_files('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par')
path_list_training = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training')

valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
                 "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
                 "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

#################################### DYNAMIC DATA STRUCTURES (training data) ################################

# Processed version of the phon_dur_dict (defined in module model_utilities): 
# Returns: a flat dictionary. Looks like: 
# {"a" : [median_1, mean_1, (m_1 + m_1) /2], "b" : [median_2, mean_2, (m_2 + m_2) /2], ...}
def phon_dur_compressed_dict(phon_dur_dict):
	phon_dur_compressed_dict = dict( (i, []) for i in valid_phonemes)

	for phon in valid_phonemes:
		phon_dur_compressed_dict[phon] = [round(np.median(phon_dur_dict[phon]), 3)]
		phon_dur_compressed_dict[phon].append(round(np.mean(phon_dur_dict[phon]), 3))
		phon_dur_compressed_dict[phon].append(round((np.median(phon_dur_dict[phon]) + np.mean(phon_dur_dict[phon]))/2, 3))
	#print(round(np.median(phon_dur_dict["v"]), 3))
	#print(round(np.median(phon_dur_dict["aU"]), 3))
	#print(phon_dur_compressed_dict["v"])
	#print(phon_dur_compressed_dict["t"])
	return phon_dur_compressed_dict



###################################### DYNAMIC DATA STRUCTURES (testdata) ##########################################

# Returns: (type: int) the predicted duration (samples) of given phoneme based on number of phonemes in word
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
def pdur_prediction_value(datei, word_no, phoneme, model):
	pdur_compressed_dict = phon_dur_compressed_dict(model_utilities.phon_dur_dict(path_list_training))
	word_dur, phoneme_count, mau_syl_count = model_utilities.word_statistics(datei, word_no)
	#print(pdur_compressed_dict)
	try:
		pdur_prediction = int(round(pdur_compressed_dict[phoneme][model], 0))
	except:
		pdur_prediction = int(round(word_dur / phoneme_count, 0))

	return pdur_prediction

#print(pdur_prediction_value("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par", 10, "t", 0))