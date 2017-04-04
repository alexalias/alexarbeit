import re
import model_utilities
import new_SR
from collections import defaultdict

######################################################## STATIC DATA #############################################################

# Dataset used must contain only modified par-files
dataset_path = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/my_test')

# List of phonemes approximated by our models. 
# As there are also other phonetic items segmented in our database, we use this list to sort those out.
# Example of excluded phonetic items: <p:>, <usb>
valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
					"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
					"g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

vowel_list = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
				"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6"]

ctype_dict = {
"plosive" : ["b", "d", "p", "t", "k", "g"], "fricative" : ["f", "v", "s", "S", "z", "Z", "x", "h", "C"],
"nasal" : ["m", "n", "N"], "lateral" : ["l"], "japproximant" : ["j"], "other" : [ "Q", "r"]
}

wtype_dict = {
"content_words" : ["ADJA", "ADJD", "ADV", "BS", "CARD", "FM", "NN", "PTKNEG", "TRUNC", "VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP", "VAIMP", "VMPP"],
"function_words" : ["APPR", "APPRART", "APPO", "APZR", "ART", "KOUI", "KOUS", "KON", "KOKOM", "PDS", "PDAT", "PIS", "PIAT", "PIDAT", "PPER", "PPOSS", "PPOSAT",
					"PRELS", "PRELAT", "PRF", "PWS", "PWAT", "PWAV", "PROP", "PTKZU", "PTKVZ", "PTKA", "VAFIN", "VAINF", "VAPP", "VMFIN", "VMINF", "XY"],
"emph_cwords" : ["BS", "NE"],
"emph_fwords" : ["ITJ", "PTKANT"]
}

########################################################## Helpfunctions for building cart-dict ###########################################################

# Returns a list of the phonemes in current syllable and their stress_type
# Looks like: [phoneme1, stress_type1, phoneme2, stress_type2, ...]
#     e.g. for syllable /j'a:/ = [ "j", "c", "a:", "p_stress"]
def get_syl_list(datei, word_no, syl_no):
	work_file = open(datei)
	syl_list = []
	w_syl_no = set([])
	word_type = ""

	# Construct a list with the phonemes of the current syllable
	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == word_no) and (int(line.split()[6]) == syl_no):
			syl_list.append(str(line.split()[4]))
			syl_list.append(str(line.split()[5]))
	work_file.seek(0)

	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == word_no):
			w_syl_no.add(int(line.split()[6]))	
		try:
			if re.match("POS", line) and (int(line.split()[1]) == word_no):
				word_type = str(line.split()[2])
		except:
			print(str(datei)[-22:])
			if re.match("POS", line) and (int(str(line.split()[1])[:len(str(word_no))]) == word_no):
				word_type = str(line.split()[2])

	work_file.close()
	
	syl_count = len(w_syl_no)

	return syl_list, syl_count, word_type

# Returns the index of the nucleus (vowel) of the current syllable
def get_nucleus_ind(syllable_list):
	# Find the index of the phoneme nucleus (vowel), if it exists, else return "NaN"
	try:
		nucleus_ind = syllable_list.index([x for x in syllable_list if x in vowel_list][0])
	except:
		nucleus_ind = "NaN"

	return nucleus_ind


# Returns the part of the syllable in which current phoneme occurs
def get_syl_part(datei, phoneme, word_no, syl_no):
	syl_part = ""

	syl_list = get_syl_list(datei, word_no, syl_no)[0][::2]

	# Find the index of the phoneme nucleus (vowel), if it exists, else return "NaN"
	try:
		nucleus_ind = syl_list.index([x for x in syl_list if x in vowel_list][0])
	except:
		nucleus_ind = "NaN"

	# Get the index of current phoneme in syl_list
	p_index = syl_list.index([x for x in syl_list if x == phoneme][0])

	if type(nucleus_ind) == int:
		if p_index < nucleus_ind:
			syl_part = "onset"
		elif p_index == nucleus_ind:
			syl_part = "nucleus"
		else: 
			syl_part = "coda"
	else:
		if len(syl_list) == 1:
			syl_part = "single"
		else:
			if p_index <= len(syl_list)/2:
				syl_part = "onset"
			else:
				syl_part = "coda"
	return syl_part

# Returns a list with information on the following phoneme
# Looks like: [word_no, phoneme, syl_no]
def get_foll_segm(datei, cursor):
	work_file = open(datei)
	zeile = 0
	foll_segm_list = []

	for line in work_file:
		zeile += 1

		if re.match("MAU", line) and zeile == (cursor+1) and (str(line.split()[4]) in valid_phonemes):
			foll_segm_list.append(int(line.split()[3]))
			foll_segm_list.append(str(line.split()[4]))
			foll_segm_list.append(int(line.split()[6]))
	return foll_segm_list

########################################################## DICTIONARY FOR CART (dynamic) ###########################################################

def cart_dict(dataset_path):
	p_dict = defaultdict(list)
	memo_list = []

	for datei in dataset_path:
		work_file = open(datei)
		word_count_set = set([])
		zeile = 0

		for line in work_file:
			zeile += 1

			if re.match("ORT", line):
				word_count_set.add(int(line.split()[1]))

			if re.match("MAU", line):
				if str(line.split()[4]) in valid_phonemes:
					p_key = str(line.split()[4])

					# Here we fill the dictionary with information from each file
					# Phoneme id
					p_dict[p_key].append(str(line.split()[4]))

					# Filename just for the record
					p_dict[p_key].append(str(datei)[-22:])

					# Phoneme type: v (vowel) or c (consonant)
					# Phoneme articulation type: v (vowel),
					if p_key in vowel_list:
						p_dict[p_key].append("v")
						p_dict[p_key].append("v")
					else:
						p_dict[p_key].append("c")

						# Phoneme articulation type: v (vowel), p (plosive), f (fricative), n (nasal), l (lateral), j (approximant), o (other)
						p_dict[p_key].append([ key[0] for key, value in ctype_dict.items() if p_key in value][0])

					# Syllable information
					# If initial position in syllable: y (yes), n (no)
					if len(memo_list) > 0:
						if memo_list[0] == int(line.split()[3]):
							if memo_list[3] == int(line.split()[6]):
								p_dict[p_key].append("n")
							else:
								p_dict[p_key].append("y")
						else:
							p_dict[p_key].append("y")
					else:
						p_dict[p_key].append("y")

					# Which syllable part contains current phoneme: onset, nucleus, coda, single
					p_dict[p_key].append(get_syl_part(datei, p_key, int(line.split()[3]), int(line.split()[6])))

					# Syllable stress: p_stress, s_stress, none
					syl_list, syl_count, word_type = get_syl_list(datei, int(line.split()[3]), int(line.split()[6]))
					nucleus_ind = get_nucleus_ind(syl_list)
					if nucleus_ind != "NaN":
						p_dict[p_key].append(syl_list[nucleus_ind+1])

					else:
						p_dict[p_key].append("none")

					# Place of the syllable in word: w_initial, w_final, w_middle
					if int(line.split()[6]) == 0:
						p_dict[p_key].append("w_initial")
					elif int(line.split()[6]) == (syl_count-1):
						p_dict[p_key].append("w_final")
					else:
						p_dict[p_key].append("w_middle")

					# Word information
					# Word type: content, function, emph_content, emph_function, other (for w_types not in dict)
					if word_type == "":
						p_dict[p_key].append("emph_fwords")
					else:
						try:
							p_dict[p_key].append([ key for key,value in wtype_dict.items() if word_type in value][0])
						except:
							p_dict[p_key].append("other")
					
					# Number of syllables in current word
					p_dict[p_key].append(syl_count)

					# Word position in phrase: initial, middle, final, single
					if len(word_count_set) == 1:
					 	p_dict[p_key].append("single")
					else:
						if int(line.split()[3]) == 0:
							p_dict[p_key].append("w_initial")
						elif int(line.split()[3]) == len(word_count_set)-1:
							p_dict[p_key].append("w_final")
						else:
							p_dict[p_key].append("w_middle")

					# Context information
					# Realised previous segment type: v (vowel), c (consonant), none (no previous segment)
					# and articulation type
					if len(memo_list) > 0:
						if memo_list[1] in vowel_list:
							p_dict[p_key].append("v")
							p_dict[p_key].append("v")
						else:
							p_dict[p_key].append("c")

							# Realised previous articulation type in case of consonants
							p_dict[p_key].append([ key[0] for key, value in ctype_dict.items() if memo_list[1] in value][0])
					else:
						p_dict[p_key].append("none")
						p_dict[p_key].append("none")

					# Realised following segment type: v (vowel), c (consonant), none (no other phoneme follows)
					#  and manner of articulation
					#  and if voiced
					following_phoneme = get_foll_segm(datei, zeile)
					if len(following_phoneme) > 0:
						if following_phoneme[1] in vowel_list:
							p_dict[p_key].append("v")
							p_dict[p_key].append("v")
							p_dict[p_key].append("v")
						else:
							p_dict[p_key].append("c")

							# Realised following articulation type in case of consonants
							p_dict[p_key].append([ key[0] for key, value in ctype_dict.items() if following_phoneme[1] in value][0])

							# If realised following phoneme is a voiced consonant: y (yes), n (no)
							if following_phoneme[1] in ["v", "z", "Z", "b", "d", "g"]:
								p_dict[p_key].append("y")
							else:
								p_dict[p_key].append("n")
					else:
						p_dict[p_key].append("none")
						p_dict[p_key].append("none")
						p_dict[p_key].append("none")

					# The syllable part to which the following phoneme belongs
					if len(following_phoneme) > 0:
						p_dict[p_key].append(get_syl_part(datei, following_phoneme[1], following_phoneme[0], following_phoneme[2]))
					else:
						p_dict[p_key].append("none")

					# Speech rate calculated as word_duration / phoneme_count_in_word
					p_dict[p_key].append(new_SR.get_word_SR(datei, int(line.split()[3]))[0])

					# Duration of current phoneme in msec
					p_dict[p_key].append(round(int(line.split()[2]) * 0.0625, 2))

					# Clear memory
					memo_list.clear()
					# Add information of current line to be available for the next line
					# Looks like: [word_no(integer), phoneme_name, stress_type, syllable_no(integer)]
					memo_list.append(int(line.split()[3]))
					memo_list.append(str(line.split()[4]))
					memo_list.append(str(line.split()[5]))
					memo_list.append(int(line.split()[6]))
		work_file.close()

	return p_dict