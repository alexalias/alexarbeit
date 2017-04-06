import re
from collections import defaultdict

diph = ["aI", "aU", "OY"]
vowels = ["a", "A", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "@" , "6", "a:", "a~:", "e:", "E:", "i:", "o:", "u:", "y:", "2:"]
consonants = ["z", "S", "Z", "C", "x", "N", "b", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

# Returns the position of the syllable containing phoneme inside word:
# - "w_initial" = 1st syllable, "w_final" = last syllable, "w_middle" = between 1st and last syll
# - "one_s" = if it's a one syllable word
# The counting of syllable is done on actually realized syllables! (not the canonical transcription)
def syl_position(datei, word_no, cursor):
	#print("Cursor: " + str(cursor))
	syls_word = get_sylsplit_word(datei, word_no)
	w1, w2 = mau_split(datei, word_no, cursor)
	mau1, mau2, sylsplit_word = prepare_strings(w1, w2, syls_word)
	#print("MAU1: " + mau1)
	if sylsplit_word != "":
		syl_dict = compare_strings(mau1+mau2, sylsplit_word)

		#print(syl_dict.keys())
		first_syl = min(syl_dict.keys())
		last_syl = max(syl_dict.keys())
		#print("Last syl: " + str(last_syl))

		if first_syl != 0:
			x = 0
			for i in range (first_syl, last_syl+1):
				syl_dict[x] = syl_dict.pop(i)
				x += 1
			last_syl = max(syl_dict.keys())
		#print("New last syl: " + str(last_syl))
		#print(syl_dict)
		try:
			syl_no = get_syl(mau1.index(mau1[-1]), syl_dict)-1
		except:
			syl_no = 0
		else:
			syl_no = 0
		#print("Syl no: " + str(syl_no))
	else:
		first_syl, last_syl = 0, 0

	inword_pos = ""
	if first_syl != last_syl:
		if syl_no == 0:
			inword_pos = "w_initial"
		elif syl_no >= last_syl:
			inword_pos = "w_final"
		else:
			inword_pos = "w_middle"
	else:
		inword_pos = "one_s"

	return inword_pos


# Based on the word number searches for the orthografical transcription of the given word,
# 	this will be used afterwards for searching in the syl-file.
# Returns the phonetic transcription with unified syllable markings from the syl.lex - file.
def get_sylsplit_word(datei, word_no):
	work_file = open(datei)
	syl_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/syl.lex")
	ORT_word = ""
	sylsplit_word = ""
	new_word=""
	i = -1  # A count index
	syl_list = [] 	# To convert word for easier manipulation

	# Search the *.par file for the orthografical transcription of needed word
	for line in work_file:
		if re.match("ORT", line) and (int(line.split()[1]) == word_no):
			ORT_word = str(line.split()[2])
			break
	#print(ORT_word)

	# Search the *.lex file for the phonetical transcription with syllable markings
	#  and eliminate alternative transcriptions
	for line in syl_file:
		if re.match(ORT_word+"\t", line):
			sylsplit_word = str(line.split()[1])
	if ";" in sylsplit_word:
		sylsplit_word = sylsplit_word[:sylsplit_word.find(";")]
	for el in sylsplit_word:
		syl_list.append(el)

	# Replace syllable markings other than ".":
	#  - #, when nicht in context: ".consonant#" or first # in "#+s#" (e.g. Arbeitstreffen)
	for el in syl_list:
		i += 1
		if el == "#":
			try:
				if (sylsplit_word[i-1] in consonants) and (sylsplit_word[i-2] =="."):
					continue
				elif (sylsplit_word[i+1] == "+") and (sylsplit_word[i+2] == "s") and (sylsplit_word[i+3] == "#"):
					continue
				else:
					syl_list.insert(i, ".")
					syl_list.pop(i+1)
			except:
				continue
	for el in syl_list:
		new_word += el

	work_file.close()
	syl_file.close()
	return new_word

# Generates 2 strings: 
# - first string contains all phones from given word till given phoneme-cursor position (inclusive)
# - second string contains all phones from given word after given phoneme
def mau_split(datei, word_no, cursor):
	work_file = open(datei)
	w1, w2 = "", ""
	zeile = 0
	
	for line in work_file:
		zeile += 1
		if re.match("MAU", line) and int(line.split()[3]) == word_no:
			if zeile <= cursor:
				w1 += line.split()[4]
			else:
				w2 += line.split()[4]

	return w1, w2

# Removes all non-letter characters from the given strings
# Returns the mau-string as 2 strings and sylsplit_string as 3 strings
#   w1 = mau-string till the phoneme of interest, including it at last position
#   w2 = rest of mau-string
#   sylsplit_word = clean sylsplit_word, just syl markings
def prepare_strings(w1, w2, sylsplit_word):
	for el in w1:
		if el == "Q":
			w1 = w1.replace("Q", "")
	for el in w2:
		if el == "Q":
			w1 = w1.replace("Q", "")
	for el in sylsplit_word:
		if el in ["+", "'", "\"", "#", "Q"]:
			sylsplit_word = sylsplit_word.replace(el, "")

	return w1, w2, sylsplit_word

# Returns a dictionary of actually realized syllables. 
# Key = syl. no. (integer), Values = substring corresponding to concat. of syl. phonemes
def compare_strings(mau12, sylsplit_word):
	mau = mau12
	#print(mau)
	syl_count = 0
	mau_syl_d = defaultdict(list)

	for el in mau:
		#print(el)
		try:
			if el == sylsplit_word[0]:
				sylsplit_word = sylsplit_word[1:]
			elif el in sylsplit_word:
				if len(mau) <= len(sylsplit_word[sylsplit_word.index(el):]):
					if "." in sylsplit_word[:sylsplit_word.index(el)]:
						syl_count +=1
					sylsplit_word = sylsplit_word[sylsplit_word.index(el)+1:]
			elif (el not in sylsplit_word) and (sylsplit_word[0] == "."):
				syl_count += 1
				sylsplit_word = sylsplit_word[1:]
		except:
			print(mau, sylsplit_word)
		mau_syl_d[syl_count].append(el)
		mau = mau[1:]

	return mau_syl_d

# Returns the number of the syllable in which our phoneme occurs
def get_syl(p_index, syl_dict):
	syl_no = -1
	x = 0

	while x <= p_index:
		x += len(syl_dict[syl_no])
		syl_no += 1
	return syl_no

#print(get_sylsplit_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_006_AAJ.par", 6))
#print(get_sylsplit_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_006_AAJ.par", 13))
#print(get_sylsplit_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 12))
#print(get_sylsplit_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 15))
#print(get_sylsplit_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 17))
#print(get_sylsplit_word("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 31))
#print(prepare_strings("Qan6", "thal", "Q''an.d6+t.h'alp"))
#print(prepare_strings("fE6aI", "nma:6n", "f6.+Q'aIn.+ba:.r#+@n"))
#print(prepare_strings("ve", "a:t6b@zu:x", "te.Qa:t6.b@.zu:x"))
print(compare_strings("an6thal", "an.d6t.halp"))	# anderthalb
print(compare_strings("fE6aInma:6n", "f6.aIn.ba:.r@n"))	# vereinbaren
print(compare_strings("b@zICtIgN", "b@.zIC.tI.g@n"))	# besichtigen
print(compare_strings("naInhalpte:gIg@s", "aI.naIn.halp.tE:.gi.g@s")) # eineinhalbtägiges
print(compare_strings("arbaItstrEfn", "a6.baIts.trE.f@n")) # Arbeitstreffen
#print(compare_strings("tE6m", "i:nmE:sIC", "tE6.mi:n.mE:.sIC"))
#print(compare_strings("neC", "stn", "n'E:Cs.t@n"))
#print(compare_strings("vea:t6b@zu:x", "te.a:.t6.b@.zu:x"))
#print(get_syl(3, "fE6aInma:6n", "f6.aIn.ba:.r@n"))
#print(get_syl(2, "aInn", "aI.n@n"))
#print(get_syl(1, "arbaItstrEfn", "a6.baIts.trE.f@n"))
#print(get_syl(2, "an6thal", "an.d6t.halp"))
#print(mau_split("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_006_AAJ.par", "b@.+z'IC.t+I.g#+@n", 6, 239))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_006_AAJ.par", 6, 234))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_006_AAJ.par", 6, 240))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_006_AAJ.par", 6, 236))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 15, 322))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 15, 325))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g009acn1_000_ABA.par", 15, 335))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par", 9, 138))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par", 9, 137))
#print(syl_position("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par", 11, 148))
