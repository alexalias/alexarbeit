import re
import model_utilities
from collections import defaultdict

######################################################## STATIC DATA #############################################################

# List of phonemes approximated by our models. 
# As there are also other phonetic items segmented in our database, we use this list to sort those out.
# Example of excluded phonetic items: <p:>, <usb>
valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
					"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
					"g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

vowel_list = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
				"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6"]

######################################################## Help Functions #############################################################

# Get a list of word-numbers to split the turn into phrases (before each number)
def get_split_list(datei):
	work_file = open(datei)
	split_list = []
	word_list = []
	a = 0
	# Variable to store the word number of the previous line
	memo_nr = 0

	# Searching MAU-tier for pauses inside turn
	for line in work_file:
		if re.match("MAU", line):
			word_list.append(int(line.split()[3]))
			if (memo_nr == -1) and (int(line.split()[3]) > 0):
				split_list.append(int(line.split()[3]))
			memo_nr = int(line.split()[3])
	
		# Searching PRO-tier for discourse split markings
		if re.match("PRO", line):
			if ";" in str(line.split()[1]):
				i = str(line.split()[1]).find(";")+1
				split_w = int(str(line.split()[1])[i:])
				split_list.append(split_w)
			else:
				split_list.append(int(line.split()[1]))
	
	if -1 in word_list:
		word_list = [x for x in word_list if x != -1]

	work_file.close()
	split_list = sorted(split_list)
	try:
		if max(word_list) > max(split_list):
			split_list.append(max(word_list))
	except:
		a += 1
		#print("Max ups")
		#print(split_list)
	return split_list

# Create dictionary of phrases in turn
# Looks like: {1 : [word_numbers belonging to phrase 1], 2 : [word_numbers belonging to phrase 2], ...}
def s_split_dict(split_list):
	ssplit_d = defaultdict(list)
	a=0
	if len(split_list) > 0:
		for i in range(len(split_list)):
			if i == 0:
				for j in range(split_list[i]):
					ssplit_d[i].append(j)
			else:
				for j in range(split_list[i-1], split_list[i]):
					ssplit_d[i].append(j)
	
	# Append last word to dict if missing
	for el in split_list:
		try:
			if len([ key for key,value in ssplit_d.items() if el in value]) == 0:
				m = max(ssplit_d.keys())
				ssplit_d[m].append(el)
		except:
			a += 1
			#print("Ups")
	return ssplit_d

#print(s_split_dict(get_split_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset/g001acn1_000_AAJ_a.par')))

# Create a complex dictionary with information for each phrase
# Looks like: {1 : [p_dur1, syl_count1, phoneme_count1, [list of contained word nrs.]], 
#				2 : [p_dur2, syl_count2, phoneme_count2, [list of contained nrs]], ...}
def c_split_dict(datei, ssplit_d):
	work_file = open(datei)
	csplit_d = defaultdict(list)
	# Memory list of previous line containing: [word_no, syl_no]
	
	if len(ssplit_d) > 0:
		memo_list = []
		#print("JA")
		for phrase in ssplit_d.keys():
			phrase_dur = 0
			syl_count = 0
			phon_count = 0
			for line in work_file:
				if re.match("MAU", line) and int(line.split()[3]) in ssplit_d[phrase]:
					phon_count += 1
					phrase_dur += int(line.split()[2])
					if len(memo_list) == 0:
						syl_count += 1
					else:
						if memo_list[0] != int(line.split()[3]):
							syl_count += 1
						elif memo_list[1] != int(line.split()[6]):
							syl_count += 1
					memo_list.clear()
					memo_list.append(int(line.split()[3]))
					memo_list.append(int(line.split()[6]))
			work_file.seek(10)
			csplit_d[phrase].append(round(phrase_dur * 0.0625, 2))
			csplit_d[phrase].append(syl_count)
			csplit_d[phrase].append(phon_count)
			csplit_d[phrase].append(ssplit_d[phrase])
	
	# If PRO tier is missing and no internal pauses in turn (aka: ssplit_d is empty)
	else:
		#print("Nein")
		phrase_dur = 0
		syl_count = 0
		phon_count = 0
		word_list = []
		m_list = []
		for line in work_file:
			if re.match("MAU", line) and (str(line.split()[4]) in valid_phonemes):
				phrase_dur += int(line.split()[2])
				phon_count += 1
				if len(m_list) == 0:
					syl_count += 1
					word_list.append(int(line.split()[3]))
				else:
					if m_list[0] != int(line.split()[3]):
						syl_count += 1
						word_list.append(int(line.split()[3]))
					elif m_list[1] != int(line.split()[6]):
						syl_count += 1

				m_list.clear()
				m_list.append(int(line.split()[3]))
				m_list.append(int(line.split()[6]))

		csplit_d[0].append(round(phrase_dur * 0.0625, 2))
		csplit_d[0].append(syl_count)
		csplit_d[0].append(phon_count)
		csplit_d[0].append(word_list)

	work_file.close()
	return csplit_d

#print(c_split_dict('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset/g001acn1_000_AAJ_a.par', s_split_dict(get_split_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset/g001acn1_000_AAJ_a.par'))))

########################################################## Speech Rate Functions #################################################################

# Phrase related speech rates:
# 1 - positive speech rates: p_phon_SR (phrase_dur / phon_count), p_syl_SR (phrase_dur / syl_count)
# 2 - negative speech rates: n_phon_SR ( phon_count / phrase_dur), n_syl_SR (syl_count / phrase_dur)
# @param ssplit_d = simple dictionary of phrases in turn, result of function: s_split_dict(split_list)
def get_phrase_SR(datei, phrase_nr, ssplit_d):
	complex_phrase_dict = c_split_dict(datei, ssplit_d)
	phrase_dur = complex_phrase_dict[phrase_nr][0]
	phon_count = complex_phrase_dict[phrase_nr][2]
	syl_count = complex_phrase_dict[phrase_nr][1]
	p_phon_PSR, p_syl_PSR, n_phon_PSR, n_syl_PSR = 0, 0, 0, 0

	p_phon_PSR = round(phrase_dur / phon_count, 2)
	p_syl_PSR = round(phrase_dur / syl_count, 2)
	n_phon_PSR = round(phon_count / phrase_dur, 2)
	n_syl_PSR = round(syl_count / phrase_dur, 2)

	return p_phon_PSR, p_syl_PSR, n_phon_PSR, n_syl_PSR

# Word related speech rates:
# 1 - positive speech rate: p_phon_WSR (word_dur / phon_count)
# 2 - negative speech rate: n_phon_WSR ( phon_count / word_dur )
def get_word_SR(datei, word_nr):
	word_dur, phon_count, syl_count = model_utilities.word_statistics(datei, word_nr)
	p_phon_WSR, n_phon_WSR = 0, 0

	p_phon_WSR = round(word_dur / phon_count, 2)
	n_phon_WSR = round(phon_count / word_dur, 2)

	return p_phon_WSR, n_phon_WSR

#SR_list = []
#for el in range(13):
#	SR_list.append(get_word_SR('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset/g001acn1_035_AAJ_a.par', el)[0])
#SR_list = [ (x/10)*2 for x in SR_list]

#print(SR_list)

#print(get_word_SR('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset/g001acn1_017_AAJ_a.par', 1)[0])