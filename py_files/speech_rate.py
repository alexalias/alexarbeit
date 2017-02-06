from __future__ import division
import re
import glob


#speech_rate2 = 0
vowel_list = ["Q", "a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "@", "6", "a:", "a~:", "e:", "E:", "i:", "o:", "u:", "y:", "2:", "OY", "aU", "aI"]

# Calculates:
# - total speech duration of a turn in seconds, without breaks,
# - total number of realized phonemes in a turn,
# - total number of words in a turn
# - total number of realized syllables in a turn,
# 
def speech_duration_pho(datei):
	#datei = open(d)
	sp_dur = 0
	phoneme_count = 0
	word_count = 0
	mau_syl_count = 0
	word = ""
	kan_syl_count = 0

	# Iterate over the lines starting with "KAN", which do not correspond to a pause.
	for line in datei:
		if re.match("KAN", line):
			word_count += 1
			word = str(line.split()[2])
			# Eliminate diphthongs, so their syllables don't get double counted
			for diph in ["aI", "aU", "OY"]:
				if diph in word:
					kan_syl_count += word.count(diph)
					word = word.replace(diph, "")
			# Count rest of vowels
			for v in vowel_list[:-12]:
				if v in word:
					kan_syl_count += word.count(v)
		# Stop search when KAN tier passed, so cursor doesn't reach EOF
		elif re.match("SYN", line):
			break

	# Iterate over the lines starting with "MAU", which do not correspond to a pause.
	for line in datei:
		if re.match("MAU", line) and ("<p" not in line):
			phoneme_count += 1 							# Get total no. of phonemes
			sp_dur += int(line.split()[2])			# Get total duration without pauses
			if str(line.split()[4]) in vowel_list:	# As syllable nuclei are always vowels, we count them to get the syllable count
				mau_syl_count += 1

	datei.seek(91)

	duration = sp_dur * 0.0000625				# Transform total duration in seconds

	return duration, phoneme_count, word_count, mau_syl_count, kan_syl_count


# Calculates speech rate per (current) file per second, not normalized. Used in phon_dict.
# Returns a number
def speech_rate(datei):
	turn_duration, phoneme_count, word_count, mau_syl_count, kan_syl_count = speech_duration_pho(datei)

	try:
		speech_rate_pho = round(phoneme_count / turn_duration, 1)
		speech_rate_w = round(word_count / (turn_duration/60), 1)
		speech_rate_msyl = round(mau_syl_count / turn_duration, 1)
		speech_rate_ksyl = round(kan_syl_count / turn_duration, 1)
	except:
	#	print(str(datei) + str(turn_duration))
		turn_duration = 1
		speech_rate_pho = round(phoneme_count / turn_duration, 1)
		speech_rate_w = 100.0
		speech_rate_msyl = round(mau_syl_count / turn_duration, 1)
		speech_rate_ksyl = round(kan_syl_count / turn_duration, 1)

	return speech_rate_pho, speech_rate_w, speech_rate_msyl, speech_rate_ksyl

# Returns:
# - word duration in miliseconds,
# - phoneme count per word
# - syllable count per word
def word_duration(datei, word_no):
	work_file = open(datei)
	word_duration = 0
	phoneme_count = 0
	mau_syl_count = 0

	for line in work_file:
		if re.match("MAU", line) and (int(line.split()[3]) == int(word_no)):
			word_duration += int(line.split()[2])
			phoneme_count += 1
			if str(line.split()[4]) in vowel_list:
				mau_syl_count += 1
	
	word_duration *= 0.0000625
	work_file.close()
	return word_duration, phoneme_count, mau_syl_count

# Calculates local speech rate based on Pfitzingers formula (SR = s * syl_rate + p * phoneme_rate)
def local_speech_rate(datei, word_no):
	w_duration, phoneme_count, syllable_count = word_duration(datei, word_no)
	w_duration = float(w_duration)
	phoneme_count = float(phoneme_count)
	syllable_count = float(syllable_count)

	phoneme_rate = round(phoneme_count/w_duration, 1)
	syll_rate = round(syllable_count/w_duration, 1)
	SR = round(0.0845*syll_rate + 0.0281*phoneme_rate, 1)

	return SR

# Gets the list of speech rate for all files (calculated in phon_dict) and 
# retrieves a list with the normalized values of these speech rates (0 to 1).
# (uses list comprehension ;) ) Not used yet.
def normalize_speech_rate(list_of_speech_rates):
	fastest_sp = max(list_of_speech_rates)
	list_of_norm_sp = [round(x/fastest_sp, 2) for x in list_of_speech_rates]
	return list_of_norm_sp


# Not used
def speech_rate_list():
	dauer = 0
	dauer2 = 0
	anzahl_phon = 0
	anzahl_phon2 = 0
	spl = []
	for file in glob.glob(r"C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g218a/g*acn*.par"):
		datei = open(file)
		#search in the open file for lines starting with "MAU"
		for line in datei:
			#Filter only lines from MAU-tier and without non-verbal segments (pause or usb)
			if re.match("MAU", line) and ("<" not in line):
				dauer += int(line.split()[2])
				anzahl_phon += 1
		#Calculate speechrate per file (dialog round) as  
		#no. of phonemes / speech time (without pauses or usb)
		dauer2 += dauer
		anzahl_phon2 += anzahl_phon
		speech_rate = round(dauer/anzahl_phon, 1)
		speech_rate2 = round(dauer2/anzahl_phon2, 1)
		spl.append(speech_rate)
		datei.close()
	return spl

#print(word_duration("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g016a/g016acn1_002_ABE.par", 0))
#print(speech_rate("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g016a/g016acn1_000_ABE.par"))
#print(speech_rate("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par/g016a/g016acn1_016_ABE.par"))

#def spl_to_excel():
#	workbook = xlsxwriter.Workbook("C:/LP/speech_rate_g218a.xlsx")
#	worksheet = workbook.add_worksheet()
#	row = 0
#	for el in speech_rate_list():
#		worksheet.write_number(row, 0, el)
#		row += 1
#	workbook.close()
#spl_to_excel()


#def spl_to_text():
#	spl_datei = open("C:/LP/spl_g218a.txt", "w")
#	for el in speech_rate_list():
#		spl_datei.write_number(el)
#	spl_datei.close()