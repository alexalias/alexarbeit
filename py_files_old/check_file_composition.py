import model_utilities
import re

dataset_path = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil_par')

dataset_list, pos_list, pro_list = [], [], []

for datei in dataset_path:
	d_name = str(datei)[-20:]
	dataset_list.append(d_name)

	work_file = open(datei)
	for line in work_file:
		if re.match("PRO", line):
			pro_list.append(d_name)
		if re.match("POS", line):
			pos_list.append(d_name)
			break
	work_file.close()

pro_set = set(pro_list)

neg_pro_list = []
for el in dataset_path:
	if el[-20:] not in pro_set:
		neg_pro_list.append(el)

w_count_list = []
for datei in neg_pro_list:
	work_file = open(datei)
	w_counter = 0
	for line in work_file:
		if re.match("ORT", line):
			w_counter += 1
	w_count_list.append(w_counter)
	work_file.close()

i = 0
nok_npro_list, ok_pro_list = [], []
for el in w_count_list:
	if el > 7:
		nok_npro_list.append(neg_pro_list[i])
	else:
		ok_pro_list.append(neg_pro_list[i])
	i += 1

nok_npro_set = set(nok_npro_list)

#print(len(dataset_list))
#print(len(pos_list))
print(len(nok_npro_list))
print(nok_npro_list[:5])
#print(nok_npro_list[:15])