import re
import model_utilities
from collections import defaultdict

word_list = ["genau", "eineinhalb", "Arbeitstreffen", "Flughafen", "auf", "einen", "fliegen", "Restaurant", "Regul"]

# Returns a dictionary of the reference words containing:
#    filename, word_duration, list of sounds and their durations in this word
# 	 All durations are in samples. Searches the complete verbmobil database.
def create_word_dict(path_list):
	word_dict = defaultdict(list)

	for datei in path_list:
		filename = str(datei)
		work_file = open(datei)
		for line in work_file:
			if re.match("ORT", line) and (line.split()[2] in word_list):
				# Filename
				word_dict[line.split()[2]].append(datei[-20:])
				# Word duration
				word_duration, phoneme_count, mau_syl_count = model_utilities.word_statistics(datei, int(line.split()[1]))
				word_dict[line.split()[2]].append(word_duration)
				#word_dict[line.split()[2]].append(int(round(word_duration/0.0000625, 0)))
				# List of word sounds and their respective durations
				word_dict[line.split()[2]].append(word_sounds(datei, line.split()[1]))
		work_file.close()
	return word_dict


# Returns a list of the sounds in the given word and their resp. durations (in samples)
#    Looks like: ["a", 648, "b", 756, ...]
def word_sounds(datei, word_no):
	work_file = open(datei)
	sound_list = []
	for line in work_file:
		if re.match("MAU", line) and int(line.split()[3]) == int(word_no):
			sound_list.append(line.split()[4])
			sound_list.append(int(line.split()[2]))

	work_file.close()
	return sound_list

word_dict = create_word_dict(model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par'))
# Create a list of durations of word "genau"
genau_dauer = word_dict["genau"][1::3]
genau_dauer = [ float(x)*0.0625 for x in genau_dauer]
#print(genau_dauer)

sound_lists = word_dict["genau"][2::3]
#print(sound_lists)
#print(sound_lists[0])
#print(len(sound_lists))

def create_word_phon_dict():
	wordSound_dict = defaultdict(list)
	k = 0
	for el in sound_lists:
		el_phones = el[::2]
		el_durations = el[1::2]
		i = 0
		for phone in el_phones:
			wordSound_dict[phone].append(el_durations[i])
			wordSound_dict[phone].append(genau_dauer[k])
			i += 1
		k += 1
	return wordSound_dict

genau_max_list = []
ind = 0
# Create a list in form:
# [w_duration, max_phone_name, dur_of_max_phone]
for el in genau_dauer:
    genau_max_list.append(el)
    max_sound_dur = max(sound_lists[ind][1::2])
    #print(max_sound_dur)
    genau_max_list.append(sound_lists[ind][sound_lists[ind].index(max_sound_dur)-1])
    #print(sound_lists[ind][sound_lists[ind].index(max_sound_dur)-1])
    genau_max_list.append(max_sound_dur)
    #print(sound_lists[ind][1::2])
    ind += 1
max_sound_list = genau_max_list[1::3]

#print(genau_max_list)
#print(create_word_dict()["genau"])
#genau_dauer = create_word_dict()["genau"][1::3]

