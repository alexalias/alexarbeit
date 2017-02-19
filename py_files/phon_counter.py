import phon_dict
import re

file_list, path_list = phon_dict.verbmo_par_files()

def phon_counter():
	count = 0
	for file in path_list:
		datei = open(file)
		for line in datei:
				if re.match("MAU", line) and (line.split()[4] == "a"):
					count += 1
				elif re.match("PRO", line):
					break
	datei.close()
	return count

print(str(phon_counter()))