#import new_phon_dict
import model_utilities
import re
import time
import numpy as np

dataset_path = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset')
#pcounter_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/pcounter_file", "w")

valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
					"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
					"g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

vowel_list = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
				"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6"]

def phon_counter(dataset_path):
	p_counter, v_counter = 0, 0
	p_dur_list = []
	for file in dataset_path:
		datei = open(file)
		for line in datei:
				if re.match("MAU", line) and (line.split()[4] in valid_phonemes):
					p_counter += 1
					p_dur_list += int(line.split()[2])
					if (line.split()[4] in vowel_list):
						v_counter += 1
				elif re.match("PRO", line):
					break
		datei.close()
	return p_counter, v_counter, p_dur_list

t1 = time.time()
p_counter, v_counter = phon_counter(dataset_path)
t2 = time.time()
print(t2 - t1)
#pcounter_file.close()

print("Total phonemes: " + str(p_counter))
print("Total vowels: " + str(v_counter))