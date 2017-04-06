import model_utilities
from collections import defaultdict

speaker_list = open('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/speaker_perDialog.txt', "w")
SL = []
speaker_list.close()
for pfad in model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par'):
	#speaker_list.write(str(pfad)[-20:-16] + "\t" + str(pfad)[-7:-4] + "\n")
	if (str(pfad)[-7:-4] not in SL) and (str(pfad)[-16] != "b"):
		SL.append(str(pfad)[-7:-4])

speaker_set = set(SL)
print(len(speaker_set))

speaker_dict = defaultdict(set)
for pfad in model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par'):
	speaker_dict[str(pfad)[-7:-4]].add(str(pfad)[-20:-15])

for speaker in speaker_dict.keys():
	speaker_list = open('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/speaker_perDialog.txt', "a")
	speaker_list.write("\n" + speaker + "\t")
	for el in speaker_dict[speaker]:
		speaker_list.write(el + "\t")
	speaker_list.close()
