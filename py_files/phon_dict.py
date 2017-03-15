import os
import glob
import fnmatch
import re
from collections import defaultdict
import stress
import speech_rate
import math
import find_syl_position

# Creates a dictionary of durations (of specific phoneme)
dur_file = open("C:/Users/alexutza_a/Abschlussarbeit/word_durations.txt", "w")
speech_rate_list = []
# List of all german .par files in verbmobil, where the recording was done acn (main scenario dialogue 
	#recorded means neckband microphone)
def verbmo_par_files():
	pattern = 'g*acn*.par'  # Pattern to be used for filtering filenames
	file_list = []			# Empty list to be populated with filenames matching pattern
	path_list = []
	for path, subfolder, filenames in os.walk('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par'):
		for filename in fnmatch.filter(filenames, pattern):
			file_list.append(filename)
			path_list.append(os.path.join(path, filename))
	return path_list#,file_list
path_list = verbmo_par_files()

# Dictionary of the given phoneme instance length in ms (keys) in Verbmobil and its attributes (values in list)
# Attributes are: Filename, Position in Speech (Start, Middle, End), Containing word, Stress, Overlapping, Speech rate
def phon_dict(phoneme_list):
	laut_schluessel = defaultdict(list)

	# Iterate over the given list of phonemes, and
	for phoneme in phoneme_list:
		#iterate over all .par files in g016a and open/close one file at a time
		#for file in glob.glob(r"C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g016a/g*acn*.par"):
		#Iterate over all .par files in the Verbmobil database and open/close one file at a time
		# search in the open file for lines starting with "MAU", and containing given phoneme.
		# Get the attributes for current phoneme, and place them as keys in the list of values.
		for file in path_list:
			datei = open(file)
			filename = str(file)
			#print(filename)
			words = total_words(datei)
			overlapping_list = overlapped_word(datei)
			sp_pho, sp_w, speech_rate_msyl, speech_rate_ksyl = speech_rate.speech_rate(datei)
			zeile = 0
			
		
			for line in datei:
				zeile += 1
				if re.match("MAU", line) and (line.split()[4] == phoneme):
					wort = int(line.split()[3])
					# Attribute: phoneme, just for easier handling
					laut_schluessel[phoneme].append(phoneme)
					# Attribute: filename 
					laut_schluessel[phoneme].append(filename[-20:])
					# Attribute: Position in Speech: Start, Middle, End
					laut_schluessel[phoneme].append(position_in_speechround(words, line))
					# Attribute: word = type of word in file
					laut_schluessel[phoneme].append(get_word(file, wort))
					# Attribute: pause = if a pause preceeds or follows the word in which the phoneme occurs: near_pause, no_pause
					laut_schluessel[phoneme].append(is_pause_near(file, wort))
					# Attribute: stress = type of stress: none, s_stress, p_stress
					laut_schluessel[phoneme].append(stress.stress_type(file, wort, phoneme, (zeile+10))) #modified zeile from +9 to +10, just for Q
					# Attribute: overlapping
					if wort in overlapping_list:
						laut_schluessel[phoneme].append("1")
					else:
						laut_schluessel[phoneme].append("0")
					# Attribute: speech rate as phonemes / sec
					laut_schluessel[phoneme].append(sp_pho)
					# Attribute: local speech rate
					laut_schluessel[phoneme].append(speech_rate.local_speech_rate(file, wort))
					#dur_file.write(file + str(speech_rate.word_duration(file, wort)) + "\n")
					# Attribute: speech rate as effective syllables / sec
					laut_schluessel[phoneme].append(speech_rate_msyl)
					# Attribute: speech rate as total syllables / sec
					#laut_schluessel[phoneme].append(speech_rate_ksyl)
					word_duration, phon_count, syl_count = speech_rate.word_duration(file, int(line.split()[3]))
					laut_schluessel[phoneme].append(round((word_duration*0.00000625)/phon_count, 4))
					# Attribute: word position: initial, not initial - only for Q
					laut_schluessel[phoneme].append(stress.find_qPosition(file, (zeile+9)))
					# Attribute: Position in word (based on syllable position): one_s, w_1, w_2, w_3
					laut_schluessel[phoneme].append(find_syl_position.syl_position(file, wort, (zeile+9)))
					# Attribute: duration (in sec)
					laut_schluessel[phoneme].append(int(line.split()[2]))
					#laut_schluessel[phoneme].append(round(freq_to_ms(int(line.split()[2])/1000), 4))
			#datei.seek(91)
			datei.close()
	return laut_schluessel
	#, speech_rate_list


# Get attribute position_in_speech_round. 
# Values: starting word(s), middle word(s), end word(s)
def position_in_speechround(total_words, line):
	if int(line.split()[3]) in [0, 1]:
		position_in_speechround = "Start_word"
	elif int(line.split()[3]) in [total_words, total_words-1]:
		position_in_speechround = "End_word"
	else:
		position_in_speechround = "Middle_word"
	return position_in_speechround

# Get list of overlapped word in current file
def overlapped_word(datei):
	list_of_overlapped_words = []

	for line in datei:
		if re.match("SUP", line):
			list_of_overlapped_words.append(line.split()[1])

	# sets back cursor position after header
	datei.seek(91)

	return list_of_overlapped_words


# Returns the type of the word in which the current phoneme occurs. 
# For non-listed types returns the actual word.
# Opens and closes another instance of the current file in order to search these.
def get_word(datei, word_number):
	word = ""
	work_file = open(datei)
	for line in work_file:
		if re.match("POS", line) and (str(word_number) in line): # check if type of word exists, and returns type if true
			word = line.split()[2]
			break
	
	work_file.seek(91)	# set back cursor after header
	if word == "":
		for line in work_file:
			if re.match("ORT", line) and (str(word_number) in line): # search actual word for non-listed types
				word = line.split()[2]
				break
	work_file.close()
	return word

# Check if the current word is placed next to a pause
# Returns "near_pause" for true, and "no_pause" for false
def is_pause_near(datei, word_number):
	next_to_pause = ""
	work_file = open(datei)
	word_number = int(word_number)
	
	# Place cursor at the start of first line of previous word
	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3] == (word_number - 1))):
			break

	# Place cursor at the start of first line after our previous word
	while re.match("MAU", line) and int(line.split()[3]) == (word_number - 1):
		line = work_file.readline()

	# Dummy first check
	if word_number == 0:
		next_to_pause = "near_pause"
	# Check if <p:> preceeds our word of interest
	elif re.match("MAU", line) and int(line.split()[3]) == -1:
		next_to_pause = "near_pause"
	elif re.match("MAU", line): 
		# Place cursor at the start of first line after our word of interest
		while int(line.split()[3]) == word_number:
			line = work_file.readline()
		# Check if <p:> follows our word of interest
		if int(line.split()[3]) == -1:
			next_to_pause = "near_pause"
		else:
			next_to_pause = "no_pause"
	else:
		next_to_pause = "no_pause"
	work_file.close()
	return next_to_pause

# Converts no of samples into milliseconds
def freq_to_ms(duration_in_samples):
	duration = round((duration_in_samples * 0.0625), 2)
	return duration

# Retrieves total no of words in file (datei), to help calculate word position in speech round
def total_words(datei):
	no_of_words = []

	# create list with number of words
	for line in datei:
		if re.match("MAU", line):
			no_of_words.append(int(line.split()[3]))

	# select max number of words to get total count
	words = max(no_of_words)
	# sets back cursor position after header
	datei.seek(91)
	return words
d = phon_dict(["a:"])
print(d["a:"][:65])
#print(p_rank_in_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g016a/g016acn1_016_ABE.par", 11, "a", 410))
#print(stress_type("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g016a/g016acn1_016_ABE.par", 11, "a", 407))