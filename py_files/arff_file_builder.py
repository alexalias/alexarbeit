import phon_dict
import fileinput
import re
import os
import sys
import time

# Generates an almost ready for processing with weka text file. 

# List of phonemes to search for
phoneme_list = ["Q"]
# All diphthongs:
#phoneme_list = ["OY", "aU", "aI"]
# All long vowels:
#phoneme_list = ["a:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "a~:"]
# All vowels:
#phoneme_list = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "OY", "aU", "aI"]

# Get the dictionary of phonemes (keys) and their attributes (values)
phon_dict = phon_dict.phon_dict(phoneme_list)
#dict_of_lengths = duration_dict.phon_dict(phoneme_list)

# Put all dict items in one list
dict_list = []
for el in phoneme_list:
	dict_list += phon_dict[el]

# Get the labels for the attribute: word
word_list = set(dict_list[3::13])


#test_file = open("C:/Users/alexutza_a/Abschlussarbeit/sp_kurzes_a.txt", "w") -> gibt falsche Anzahl von speech rates
arff_file = open("C:/Users/alexutza_a/Abschlussarbeit/wekadateien/Q.txt", "w")

arff_file.write("% ARFF file for Verbmobil\n% Phoneme: all_vowels_noSchwa\n%\n@relation glottal_stop\n\n% List of attributes:\n%\n")
arff_file.write("% Duration is expressed in seconds\n")

arff_file.write("@attribute phoneme { Q") 
#for el in phoneme_list:
#	arff_file.write(el + ", ")
arff_file.write( " }\n")

arff_file.write("@attribute filename string\n")
arff_file.write("@attribute speech_position { Start_word, Middle_word, End_word }\n")
arff_file.write("@attribute word { " )
for el in word_list:
	arff_file.write(el + ", ")

arff_file.write( " }\n")
arff_file.write("@attribute pause { near_pause, no_pause }\n")
arff_file.write("@attribute stress { none, p_stress, s_stress }\n")
arff_file.write("@attribute overlapping { 1, 0 }\n")
arff_file.write("@attribute speech_rate_pho numeric\n")
arff_file.write("@attribute local_speech_rate numeric\n")
arff_file.write("@attribute speech_rate_msyl numeric\n")
arff_file.write("@attribute speech_rate_ksyl numeric\n")
#arff_file.write("@attribute word_position {0, 1}\n")
arff_file.write("@attribute syl_position { one_s, w_initial, w_middle, w_final }\n")
arff_file.write("@attribute duration numeric\n\n")
arff_file.write("@data\n%\n")


# Writes all duration-instance related attributes to a txt file
# Param good_flat_list: list with duration attributes in the right formatting, ready for data mining,
# e.g. normalized speech rate values
def write_data_in_arff_file(ph_list):
	for el in dict_list:
		if (dict_list.index(el) + 1) % 13 == 0:
			arff_file.write(str(el) + "\n")
		else:
			arff_file.write(str(el) + ", ")
	arff_file.close()

write_data_in_arff_file(dict_list)

# Must iterate the writing of the text file, otherwise not all data gets written
#while len(norm_flat_list) > 0:
#	write_data_in_arff_file(norm_flat_list)
#	arff_file = open("C:/Users/alexutza_a/Abschlussarbeit/wekadateien/diphthongs.txt", "a")
#	#print(len(norm_flat_list))
	#print(len(duration_list_per_phoneme))
#arff_file.close()