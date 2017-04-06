# Erstellt eine Datei mit 2 Spalten:
# 1. orthografische Form des Wortes
# 2. phonetische Form des Wortes, mit Silbentrennzeichen.

lex_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/verbmobil.lex")
syl_file = open("C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/syl.lex", "w")

for line in lex_file:
	syl_file.write(line.split()[0] + "\t")
	syl_file.write(line.split()[3] + "\n")