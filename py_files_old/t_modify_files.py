import os
import re
import model_utilities
import stress
import get_syllables
import time

dataset = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Rest')
vowel_list = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6"]

t1 = time.time()
# Returns a list containing the syllable number for each phoneme in given word number
# Looks like: [0011] for the word genau realized as /g@naU/
def get_syl_no(datei, word_no):
	syl_dict = get_syllables.syl_position(datei, word_no)
	syl_numbers_list = []
	key_list = sorted(syl_dict.keys())
	#print(syl_dict)
	i = 0
	for syl_no in key_list:
		for value in syl_dict[syl_no]:
			# Consider cases where elements of diphthongs, nasals, or long vowels are listed separately in the value list
			if value not in ["~", ":", "I", "U", "Y"]:
				syl_numbers_list.append(i)
			elif value in ["I", "U"] and "a" not in syl_dict[syl_no]:
				syl_numbers_list.append(i)
			elif value == "Y" and "O" not in syl_dict[syl_no]:
				syl_numbers_list.append(i)

		i += 1
	#print(syl_numbers_list)
	return syl_numbers_list

i = 0
# Here starts the file annotation
for datei in dataset:
	if i%180 == 0:
		print(i)

	z = 0
	work_file = open(datei)
	m_file = open('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset/' + str(datei)[-20:-4] + "_a" + str(datei)[-4:], "w")
	syl_list_counter = 0
	for line in work_file:
		z += 1
		if re.match("MAU", line):
			syl_numbers_list = get_syl_no(datei, int(line.split()[3]))

			# Annotate only when no break, and syllable dictionary not empty
			if int(line.split()[3]) >= 0 and len(syl_numbers_list) > 0:
				
				# Case1: current phoneme is a vowel
				if (str(line.split()[4]) in vowel_list):
					phon_stress = stress.stress_type(datei, int(line.split()[3]), str(line.split()[4]), z)
					m_file.write(line.rstrip() + "\t" + phon_stress + "\t" + str(syl_numbers_list[syl_list_counter]) + "\n")

					if syl_list_counter < len(syl_numbers_list)-1:
						syl_list_counter += 1
					else: 
						syl_list_counter = 0

				# Case2: current phoneme is glottal stop /Q/
				elif str(line.split()[4]) == "Q":
					m_file.write(line.rstrip() + "\tc\t0\n")

				# Case3: current phoneme is a consonant
				else:
					m_file.write(line.rstrip() + "\tc" + "\t" + str(syl_numbers_list[syl_list_counter]) + "\n")
					if syl_list_counter < len(syl_numbers_list)-1:
						syl_list_counter += 1
					else: 
						syl_list_counter = 0
			
			# Annotation procedure if no syl_list available for current word
			elif len(syl_numbers_list) == 0:
				# Case1: current phoneme is a vowel
				if (str(line.split()[4]) in vowel_list):
					phon_stress = stress.stress_type(datei, int(line.split()[3]), str(line.split()[4]), z)
					m_file.write(line.rstrip() + "\t" + phon_stress + "\t0\n")
					syl_list_counter = 0
				# Case2: current phoneme is not a vowel
				else:
					m_file.write(line.rstrip() + "\tc\t0\n")
					syl_list_counter = 0

			# No annotation if current MAU line contains a break
			elif int(line.split()[3]) == -1:
				m_file.write(line)
				syl_list_counter = 0

		# File lines not starting with MAU are just being copied
		else:
			m_file.write(line)
			continue
	i += 1

	m_file.close()
	work_file.close()
print(str(time.time() - t1))