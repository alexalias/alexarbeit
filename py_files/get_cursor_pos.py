import re

def cursor_pos():
	work_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test/g002acn1_000_AAJ.par")
	#work_file = open("C:/LP/ad_lesbiam.txt")
	zeile = 0
	p_zeile = []

	for line in work_file:
		zeile += 1
		if re.match("MAU", line) and (int(line.split()[3]) == 9) and (str(line.split()[4]) == "n"):
			p_zeile.append(zeile)
			print(line)
	work_file.close()
	return p_zeile
#cursor_pos()
print(cursor_pos())