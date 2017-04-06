import model_utilities
import re

dataset = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/mod_dataset')
file_error_list = []

for datei in dataset:
	w_f = open(datei)
	for line in w_f:
		if re.match("POS", line):
			if "," in str(line.split()[1]):
				file_error_list.append(str(datei)[-22:])
	w_f.close()
print(file_error_list)