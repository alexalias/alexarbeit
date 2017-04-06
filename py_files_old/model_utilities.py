import os
import fnmatch
import re
from collections import defaultdict

# This file contains help functions that are used across models

############################### STATIC DATA #################################

# List of phonemes approximated by our models. 
# As there are also other phonetic items segmented in our database, we use this list to sort those out.
# Example of excluded phonetic items: <p:>, <usb>
valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
                 "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
                 "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

vowel_list = ["Q", "a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "@", "6", "a:", "a~:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "OY", "aU", "aI"]

############################### FUNCTIONS #################################


# Return: List of all german .par filepaths in provided data set, 
#    where the recording was done acn (main scenario dialogue recorded means neckband microphone)
# @param dataset_path: (string) path to the folder containing needed files (data)
def get_path_list(dataset_path):
	pattern = 'g*acn*.par'  # Pattern to be used for filtering filenames
	path_list = []
	for path, subfolder, filenames in os.walk(dataset_path):
		for filename in fnmatch.filter(filenames, pattern):
			path_list.append(os.path.join(path, filename))
	return path_list


# Creates a flat dictionary of phonemes and their durations in the given dataset
# Return looks like: {"a" : [1599, 2348, 959, ...], "b" : [...], ...}
def phon_dur_dict(path_list):
    phon_dur_dict = dict( (i, []) for i in valid_phonemes)

    for datei in path_list:
        work_file = open(datei)
        
        for line in work_file:
            if re.match("MAU", line) and (str(line.split()[4]) in valid_phonemes):
                phon_dur_dict[str(line.split()[4])].append(int(line.split()[2]))
        work_file.close()
    #print(l)
    #print(len(phon_dur_dict["Z"]))
    #print(len(phon_dur_dict["a~:"]))
    return phon_dur_dict


# Creates a nested dict of phoneme proportions in words of specific lengths (as no of phonemes) - w_dur in samples
# Returns: a dictionary
# Looks like: {"a" : {1 : [w_dur1, pho_dur1, pho_prop1, w_dur2, pho_dur2, pho_prop2, ...], 2: [...], ...}, 
#              "b" : {1 : [w_dur1, pho_dur1, pho_prop1, w_dur2, pho_dur2, pho_prop2, ...], 2: [...], ...}, 
#               ...}
# @param path_list: list of paths to the files in the (training) dataset to be used
def phon_wordleng_dict(path_list):
    simple_phoprop_dict = dict( (i, defaultdict(list)) for i in valid_phonemes) # the dict to be returned
    
    #Iterate over the training files
    for datei in path_list:
        work_file = open(datei)
        for line in work_file:
            if re.match("MAU", line):
                if (str(line.split()[4]) in valid_phonemes):
                    w_dur, phon_count, syl_count = word_statistics(datei, int(line.split()[3]))
                    simple_phoprop_dict[str(line.split()[4])][phon_count].append(w_dur)
                    simple_phoprop_dict[str(line.split()[4])][phon_count].append(int(line.split()[2]))
                    simple_phoprop_dict[str(line.split()[4])][phon_count].append( round(int(line.split()[2])/w_dur, 3))
        work_file.close()  
    return simple_phoprop_dict


# Returns:
#  - word duration in samples,
#  - phoneme count per word, and
#  - syllable count per word.
def word_statistics(datei, word_no):
	work_file = open(datei)
	word_duration = 0
	phoneme_count = 0
	mau_syl_count = 0

	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == int(word_no)):
			#print(line)
			word_duration += int(line.split()[2])
			phoneme_count += 1
			if str(line.split()[4]) in vowel_list:
				mau_syl_count += 1
	
	word_duration *= 0.0625
	work_file.close()

	return word_duration, phoneme_count, mau_syl_count

#print(len(phon_dur_dict(get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training'))))
#print(len(phon_wordleng_dict(get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training'))))