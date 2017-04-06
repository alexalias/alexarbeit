import re

short_vowels = ["a", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2"]

# Sets the context of search at file level and finds the right word number
# Returns the type of stress that falls on the given vowel of the given file of the given word 
# none (unstressed), s_stress (secondary), p_stress (primary)
def stress_type(datei, word_number, phoneme, cursor):
	work_file = open(datei)
	word_no = int(word_number)
	z = 0
#	Instructions for Q to get the stress of the following phoeneme
#	for line in work_file:
#		z += 1
#		if z == (cursor):
#			phoneme = line.split()[4]
			#print(phoneme)
		
	mau_rank = p_rank_in_mau(work_file, word_no, phoneme, cursor)
	#print("MAU-rank: " + str(mau_rank))
	#stress_type = ""
	#word = ""
	
	for line in work_file:	
		if re.match("KAN", line) and (int(line.split()[1]) == word_no):
			word = str(line.split()[2])
			stress_type = set_stress(datei, word, phoneme, word_number, mau_rank, cursor)
			break
		else:
			continue

	work_file.close()
	return stress_type

# Sets the context of search at word level
# Actually determines the stress of the given phoneme in the given word.
def set_stress(datei, word, phoneme, word_number, mau_rank, cursor):
	stress_type = ""
	p_index = -1
	mau, kan = kan_mau_string_builder(datei, word, word_number)

	# Schwa is never stressed
	if phoneme in ["@", "6"]:
		stress_type = "none"
	# Q occurs always before a vowel, either at word initial position or inside word-composita bevor a stressed vowel morpheme initial
	# As cases with more than two Q in a word are extremely rare in our database, we decided to make only 2 distinctions for its position
	elif phoneme == "Q":
		qPosition = find_qPosition(datei, cursor)
		stress_type = set_QLabel(qPosition, kan)
	# Set stress for short vowel monophthongs (except "a~", which is included in the diphthong search)
	else:#if phoneme in short_vowels:
		stress_type = short_mono_stress(mau, kan, mau_rank, phoneme)

	return stress_type

# Sets the context of search at phoneme level (we already are inside the given word, at the correct position inside the word)
# Checks inside the given word the type of stress at the given index position.
def set_label(index, word):
	stress_type = ""

	try:
		if word[index - 1] == "'":
			stress_type = "p_stress"
		elif word[index - 1] == "\"":
			stress_type = "s_stress"
		else:
			stress_type = "none"
	except:
		stress_type = "none"

	return stress_type

# Checks the type of stress of the vowel after the glottal stop
def set_QLabel(qPosition, kan_word):
	stress_type = ""
	index = 0

	# Gets the index of Q if the occurence is inside word
	if qPosition == 1:
		index = kan_word[1:].find("Q")

	# Set label based on the 2 possible situations
	if kan_word[index+1] == "'":
		stress_type = "p_stress"
	elif kan_word[index + 1] == "\"":
		stress_type = "s_stress"
	else:
		stress_type = "none"

	return stress_type

# Puts the current word in MAU and KAN tiers in two strings, for easier comparison
def kan_mau_string_builder(datei, word, word_number):
	datei = open(datei)

	# Define kan as the current word in the KAN tier in string format
	kan = word
	
	# Put the spoken phonemes of word (MAU tier) in a string
	mau = ""
	for line in datei:
		if re.match("MAU", line) and int(line.split()[3]) == int(word_number):
			mau += str(line.split()[4])

	return mau, kan

# Checks if the glottal stop occurs inside word (1) or at the beginning of the word (0)
def find_qPosition(datei, cursor):
	datei = open(datei)
	zeile = 0
	word_number_prev_line = 0
	qPosition = 0

	for line in datei:
		zeile += 1
		if re.match("MAU", line) and (zeile == cursor-1):
			word_number_prev_line = int(line.split()[3])
		if re.match("MAU", line) and (zeile == cursor):
			if int(line.split()[3]) == word_number_prev_line:
				qPosition = 1
			break
	datei.close()
	return qPosition

# Memory for the short_mono_stress function, as it uses recursion
stress_memo = []

# Sets the stress label for the short vowel monophthongs
# One constraint: vowel inside a sequence of identical syllables, and the former one is dropped
def short_mono_stress(mau, kan, mau_rank, phoneme):
	# Count of phonemes in mau and kan strings
	count_m = mau.count(phoneme) 
	count_k = kan.count(phoneme)
	stress_type = ""

	if mau_rank == 0:
		# If given phoneme has same count in both strings, 
		#  then we can simply search for the needed occurence in the kan string, no other checks necessary
		if count_m == count_k: 
			#print("ok")
			k_index = kan.find(phoneme)
			stress_type = set_label(k_index, kan)

		# If a < count of phoneme has been realized, we must check for dropped vowels
		elif count_m < count_k:
			occur = kan.find(phoneme)
			# If the phoneme occurrence is at the same place in word as in the mau tier,
			#  then the dropped ones occur afterwards and don't interest us anymore
			# @ Param: Do never modify the first param: 1 !!!
			if right_place_check(1, mau, mau.find(phoneme), kan, occur, phoneme):
				stress_type = set_label(occur, kan)

			# If the given phoneme occurence in kan is not at the same place in word as in the mau tier,
			#  then it's a dropped one, and we have to eliminate it from the string, so it doesn't falsify the stress label
			else:
				if len(kan) > 0:
					kan = kan[occur+1:]
					short_mono_stress(mau, kan, mau_rank, phoneme)
				# Theoretical case that the phoneme doesn't occur in mau, but would be search it in kan 
				#  impossible case for the current code configuration, but considered because of the recursion
				else: 
					stress_type = "none"

		# This case can never occur in real life.
		# We take none as default value, because, if some vowel has been modified, that it must be rather unstressed
		else: 
			stress_type = "none"
		#print("Stress type " + stress_type)
	# When lowering the rank we chose to reduce only the mau_list, as the right_place test should eliminate  
	#  most of the not relevant phoneme occurences in the kan string.
	else:
		mau_rank -= 1
		mau = mau[mau.find(phoneme)+1:]
		short_mono_stress(mau, kan, mau_rank, phoneme)
	if stress_type != "":
		stress_memo.insert(0, stress_type)

	return stress_memo[0]

place_memo = [0]
# Checks if the current mau phoneme is in the same place as the found kan phoneme
# For this, it compares one character before or one character after current phoneme
def right_place_check(i, mau, m_i, kan, k_i, phoneme):
	check = None

	try:
		if m_i > 0:
			if kan[k_i-i].isalpha() or kan[k_i-i].isdigit():
				if mau[m_i - 1] == kan[k_i - i]:
					check = 1
				else:
					check = 0
			else:
				i += 1
				right_place_check(i, mau, m_i, kan, k_i, phoneme)

		elif m_i == 0:
			if kan[k_i+i].isalpha() or kan[k_i+i].isdigit():				
				if mau[m_i + 1] == kan[k_i + i]:
					check = 1
				else: 
					check = 0
			else:	
				i += 1
				right_place_check(i, mau, m_i, kan, k_i, phoneme)
	except: 
		check = 1

	# Fill memory list with real result of the check:
	if check != None:
		if place_memo[0] != check:
			place_memo.insert(0, check)
	
	return place_memo[0]


# Returns rank of given phoneme in word (if it's the first occurence, or the second, etc.)
def p_rank_in_mau(datei, word_number, phoneme, cursor):
	#datei = open(datei)
	mau_rank = 0
	zeile = 0

	for line in datei:
		zeile += 1
		if re.match("MAU", line)  and (zeile == cursor):
			break
		elif re.match("MAU", line) and (int(line.split()[3]) == word_number) and (zeile < cursor):
			if phoneme in str(line.split()[4]):
				mau_rank += 1
				continue
		elif zeile > cursor:
			break
	datei.seek(90)

	return mau_rank

#print(short_mono_stress("anf", "Q'anfaN", 0, "a"))
#print(short_mono_stress("naInhal", "Q\"aIn#aIn#h'alp", 1, "a"))
#print(p_rank_in_mau("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g431a/g431acn2_013_AMD.par", 13, "a", 374))
#print(short_mono_stress("naInhalp", "Q\"aIn#aIn#h'alp", 1, "aI"))
#print(p_rank_in_mau("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g431a/g431acn2_013_AMD.par", 13, "a", 371))
#print(short_mono_stress("an6thalp", "Q\"and6thalp", 1, "a"))
#print(short_mono_stress("an6thalp", "Qand6th\"alpa", 1, "a"))
#print(short_mono_stress("definiti:f", "definit'i:f", 0, "i:"))
#print(p_rank_in_mau("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g419a/g419acn1_012_ALW.par", 9, "i:", 155))
#print(set_stress("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g419a/g419acn1_012_ALW.par", "definit'i:f", "i:", 9, 0, 155))
#print(stress_type("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g419a/g419acn1_012_ALW.par", 9,  "i:", 155))
#print(stress_type("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g419a/g419acn1_016_ALW.par", 4, "Q", 116))