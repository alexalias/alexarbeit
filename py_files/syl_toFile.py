import os
import re

def verbmo_par_files():
	pattern = 'g*acn*.par'  # Pattern to be used for filtering filenames
	file_list = []			# Empty list to be populated with filenames matching pattern
	path_list = []
	for path, subfolder, filenames in os.walk('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training'):
		for filename in fnmatch.filter(filenames, pattern):
			file_list.append(filename)
			path_list.append(os.path.join(path, filename))
	return path_list#,file_list
path_list = verbmo_par_files()

def add_sylInfo_toFile():
	for elem in path_list:
		datei = open(elem, "a")
		