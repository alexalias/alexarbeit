import re
import numpy as np
from collections import defaultdict
import model_utilities

# This is a phoneme duration prediction model for varying word duration.
# It supposes we know the target word duration, and is based only on that feature.
#
# Before predicting phoneme duration, the phoneme is classified in one of the following categories: 
#		diphthong, long_vowel, short_vowel, etc -> wehere the class members don't correspond completely to the ones listed in the grammar books.
# Information from the training data is used to compute the steak each class member takes in a n-phoneme-long word. (? or maybe better if this is also resumed they way pred-values are ?)
#
# Predicted value = steak*w_dur/class-member-count-in-word

###################################################### START ##################################################################


############## STATIC DATA STRUCTURES (not dataset specific) ##################################


# Create list of filepaths to explore. This one uses entire data set, for exploration purposes.
# path_list_training = verbmo_par_files('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par')
path_list_training = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training')

# Classification of phonemes used by this model
phon_class_dict = {"diphthong" : ["aI", "aU", "OY"], "long_vowels" : ["a:", "E:", "e:", "i:", "2:", "@", "m", "k", "N"], 
					"short_vowels" : ["a", "u:", "o:", "e", "O", "E", "C", "6", "U", "f", "y", "o", "S", "j", "y:"], 
					"cons_allg" : ["x", "h", "l", "n", "I", "9", "z", "s", "Y", "v", "t"], "short_cons" : ["p", "b", "d", "g"], 
					"others" : ["Q", "r"]}

valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
                 "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
                 "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

#################################### DYNAMIC DATA STRUCTURES (training data) ################################

# Processed version of the phon_wordleng_dict: 
#    - the phoneme keys are grouped according to the classes of the phon_class_dict
#    - the value-lists of the inner dict include only the phoneme proportions for the given word length (inner key)
# Returns: a dictionary. Looks like: 
# {"diphthongs" : { 1 : [0.5, 0.62, 0.55, ...], 2 : [0.4, 0.42, 0.45, ...] ...}, 
#  "long_vowels" : { 1 : [...], ...}, ...}
def pcat_dict(phon_wordleng_dic):
	pcat_dict = dict( (i, defaultdict(list)) for i in phon_class_dict.keys() )

	# Incorporate all phoneme proportion lists for each phoneme class:
	#    - the phoneme keys are grouped according to the classes of the phon_class_dict
	#    - the value-lists of the inner dict include only the phoneme proportions for the given word length (inner key)
	# Looks like: 
	# {"diphthongs" : { 1 : [0.5, 0.62, 0.55, ...], 2 : [0.4, 0.42, 0.45, ...] ...}, 
	#  "long_vowels" : { 1 : [...], ...}, ...}
	for phoneme in phon_wordleng_dic.keys():
		p_category = ([ key for key,val in phon_class_dict.items() if phoneme in val ] + ["long_vowels"])[0]
		for w_leng in phon_wordleng_dic[phoneme].keys():
			pcat_dict[p_category][w_leng] += phon_wordleng_dic[phoneme][w_leng][2::3]

	# Reduce the proportion lists to lists containing the coresponding median, mean, and mean+median/2
	# Looks like: 
	#   {"diphthongs" : { 1 : [median1, mean1, (m1+m1)/2 ], 2 : [median2, mean2, (m2+m2)/2] ...}, 
	#    "long_vowels" : { 1 : [median, mean, (m+m)/2], ...}, ...}
	pcat_dict_reduced = dict( (j, defaultdict(list)) for j in pcat_dict.keys())
	for categ in pcat_dict_reduced.keys():
		for w_leng in pcat_dict[categ].keys():
			pcat_dict_reduced[categ][w_leng].append(round(np.median(pcat_dict[categ][w_leng]), 3))   # append median (model = 0)
			pcat_dict_reduced[categ][w_leng].append(round(np.mean(pcat_dict[categ][w_leng]), 3))     # append mean (model = 1)
			pcat_dict_reduced[categ][w_leng].append(round((np.median(pcat_dict[categ][w_leng]) + np.mean(pcat_dict[categ][w_leng]))/2, 3))   # append (median+mean)/2 (model = 2)

	return pcat_dict_reduced

# Call the dictionary from the training data
pcat_dict_reduced = pcat_dict(model_utilities.phon_wordleng_dict(path_list_training))
#print(pcat_dict_reduced["diphthong"][3])
#print(pcat_dict_reduced["others"][3])

###################################### DYNAMIC DATA STRUCTURES (testdata) ##########################################


# Wendet den pcat_dict_reduced auf dem vorgegebenen Wort ein
# Return: dictionary mit den entsprechenden phon_class steaks fuer das aktuelle Wort (erfasst in composition_dict)
# Looks like: pcat_dict_reduced, but is not nested anymore: {"diph" : [median1, mean1, (m1+m2)/2 ], "long_vowels" : [...], ...}
def class_steak(composition_dict):
	class_correction_factor = defaultdict(list)
	word_comp_dict = dict.fromkeys(composition_dict.keys(),0)
	# Umwandlung der Belegung von composition_dict in binären Werten (0, 1)
	for cat in composition_dict.keys():
		if composition_dict[cat] >= 1:
			word_comp_dict[cat] = 1
	
	cat_overview = word_comp_dict.items()
	filled_cat = sum([x[1] for x in cat_overview])  # returns count of filled categories in composition_dict
	
	# Fill the dictionary of filled categ. in word with the corresponding values for median, mean, half(median+mean)
	for cat in word_comp_dict.keys():
		if word_comp_dict[cat] != 0:
			class_correction_factor[cat] = pcat_dict_reduced[cat][filled_cat]
		else:
			class_correction_factor[cat] = 0
	
	return class_correction_factor

# Return: A dictionary of word composition. 
# Looks like: 
#     {"diph" : 1, "long_vowels" : 0, "short_vowels" : 2, "cons_allg" : 0, "short_cons" : 0, "others" : 0}
def build_composition_dict(datei, word_no):
	work_file = open(datei)

	# Initialize composition_dict with phoneme categ. as keys and default value = 0
	composition_dict = dict.fromkeys(phon_class_dict.keys(), 0)  

	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == word_no):
			try:
				phon_type = [key for key, val in phon_class_dict.items() if str(line.split()[4]) in val][0]
			except:
				phon_type = "long_vowels"
			composition_dict[phon_type] += 1
	work_file.close()
	return composition_dict
#print(build_composition_dict("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test1/g002acn1_000_AAJ.par", 10))

# Returns: (type: int) the predicted duration (samples) of given phoneme based on word composition
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
def pdur_prediction_value(datei, word_no, phoneme, model):
	work_file = open(datei)
	composition_dict = build_composition_dict(datei, word_no)
	word_dur, word_leng = 0, 0

	# Get needed information about the given phoneme instance and word in which it occurs
	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == word_no) and (str(line.split()[4]) in valid_phonemes):
			word_dur += int(line.split()[2])
			word_leng += 1
			try:
				phon_type = [key for key, val in phon_class_dict.items() if phoneme in val][0]
			except:
				phon_type = "long_vowels"
	work_file.close()

	# Actually calculate the phon duration prediction
	pdur_prediction = int(round( ((word_dur * class_steak(composition_dict)[phon_type][model])/composition_dict[phon_type]), 0))
	
	return pdur_prediction
#print(pdur_prediction_value("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test1/g002acn1_000_AAJ.par", 10, "t", 0))