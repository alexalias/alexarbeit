import new_phon_dict
import model_utilities
import phon_list
import time

# Generates an almost ready for processing with weka text file. 

######################################################## STATIC DATA #############################################################
# Dataset used must contain only modified par-files
dataset_path = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training_a')

# List of phonemes approximated by our models. 
# As there are also other phonetic items segmented in our database, we use this list to sort those out.
# Example of excluded phonetic items: <p:>, <usb>
valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
					"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
					"g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

vowel_list = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
				"o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6"]

ctype_dict = {
"plosive" : ["b", "d", "p", "t", "k", "g"], "fricative" : ["f", "v", "s", "S", "z", "Z", "x", "h", "C"],
"nasal" : ["m", "n", "N"], "lateral" : ["l"], "japproximant" : ["j"], "other" : [ "Q", "r"]
}

wtype_dict = {
"content_words" : ["ADJA", "ADJD", "ADV", "BS", "CARD", "FM", "NN", "PTKNEG", "TRUNC", "VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP", "VAIMP", "VMPP"],
"function_words" : ["APPR", "APPRART", "APPO", "APZR", "ART", "KOUI", "KOUS", "KON", "KOKOM", "PDS", "PDAT", "PIS", "PIAT", "PIDAT", "PPER", "PPOSS", "PPOSAT",
					"PRELS", "PRELAT", "PRF", "PWS", "PWAT", "PWAV", "PROP", "PTKZU", "PTKVZ", "PTKA", "VAFIN", "VAINF", "VAPP", "VMFIN", "VMINF", "XY"],
"emph_cwords" : ["BS", "NE"],
"emph_fwords" : ["ITJ", "PTKANT"]
}

######################################################## Writing file: attribute description #############################################################

arff_file = open("C:/Users/alexutza_a/Abschlussarbeit/wekadateien/cart_min_trainAKX.txt", "w")

arff_file.write("% ARFF file for Verbmobil\n% \n@relation cart\n%\n% List of attributes:\n")
arff_file.write("% Duration is expressed in miliseconds\n%\n")

# Describing the first attribute: phoneme
for el in valid_phonemes:
	if valid_phonemes.index(el) == 0:
		arff_file.write("@attribute phoneme { " + el)
	elif valid_phonemes.index(el) < (len(valid_phonemes) - 1):
		arff_file.write(", " + el)
	else:
		arff_file.write( el + " }\n")

arff_file.write("@attribute filename string\n")
arff_file.write("@attribute phoneme_type { v, c }\n")
arff_file.write("@attribute art_manner { v, p, f, n, l, j, o }\n")
arff_file.write("@attribute init_pos_in_syl { y, n }\n")
arff_file.write("@attribute syl_part { onset, nucleus, coda, single }\n")
arff_file.write("@attribute syl_stress { p_stress, s_stress, none }\n")
arff_file.write("@attribute syl_place_in_w { w_initial, w_final, w_middle }\n")
arff_file.write("@attribute w_type { content_words, function_words, emph_content, emph_function, emph_cwords, emph_fwords, other }\n")
arff_file.write("@attribute syl_count_in_w numeric\n")
arff_file.write("@attribute w_pos_in_turn { w_initial, w_middle, w_final, single}\n")
arff_file.write("@attribute prev_p_type { v, c, none }\n")
arff_file.write("@attribute prev_p_artic { v, p, f, n, l, j, o, none }\n")
arff_file.write("@attribute foll_p_type { v, c, none }\n")
arff_file.write("@attribute foll_p_artic { v, p, f, n, l, j, o, none }\n")
arff_file.write("@attribute foll_p_voiced { v, y, n, none }\n")
arff_file.write("@attribute syl_part_foll_p { onset, nucleus, coda, single, none }\n")
arff_file.write("@attribute speech_rate numeric\n")
arff_file.write("@attribute duration numeric\n%\n")

######################################################## Writing file: data #############################################################

arff_file.write("@data\n%\n")

t1 = time.time()
# Create dictionary to be written in the arff-file
c_dict = new_phon_dict.cart_dict(dataset_path)
#cart_l = phon_list.cart_list(dataset_path)
t2 = time.time()
print("Time to create dictionary: " + str(t2 - t1))

# Combine all value lists of the dictionary into one huge list
#cart_list = []
#for phon in cart_dict.keys():
#	cart_list += cart_dict[phon]
#t3 = time.time()
#print("Time to build the list for writing: " + str(t3 - t2))

time1 = time.time()
#print("Time to get list length: " + str(time1 - t3))
#i =0
# Write elements of the cart_list to the arff_file
#for el in cart_list:
#	if (cart_list.index(el) + 1)%19 ==0:
#	if (i+1)%19 == 0:
#		arff_file.write(str(el) + "\n")
#	else:
#		arff_file.write(str(el) + ", ")
#	i += 1


for phon in c_dict.keys():
    phon_list = c_dict[phon]
    i = 0
    while (i < len(phon_list)):
        arff_file.write (", ".join([ str(x) for x in phon_list[i:i+19]]) + "\n")
        i += 19

#i = 0
#while (i < len(cart_l)):
#    arff_file.write (", ".join([ str(x) for x in cart_l[i:i+19]]) + "\n")

#    i += 19

arff_file.close()

time2 = time.time()
print("Time to write the data: " + str(time2-time1))
#