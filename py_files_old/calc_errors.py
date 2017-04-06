import performance_measures
import numpy as np
from collections import defaultdict
import pd_LSR

#phon_dict, test_dict, tm_dict = prepare_data.calculate_pho_mean(prepare_data.read_trainig_files())
# A dictionary giving the values of Mean and SD in a list for each encountered phoneme.
stat_dict = pd_LSR.phone_stats(pd_LSR.read_trainig_files())
#print(test_dict)

#testlist = prepare_data.read_testfiles()
# Looks like: ["a", 583, 0.5, "b", 12, 0.78, "a", 489, 0.12, ...]
testlist = pd_LSR.read_testfiles()
#print(testlist)

predictions = pd_LSR.create_prediction_list(testlist, stat_dict)
actual = pd_LSR.read_testfiles()[1::3]


#print(len(predictions))
#print(prepare_data.read_testfiles())
#print(len(actual))

global_rmse, mae = performance_measures.calc_error_for_data(predictions, actual)
corrCoef = performance_measures.corrCoef(predictions, actual)[0]
print(global_rmse, mae, corrCoef)


### Following is rmse calculation individually (per phoneme) ###



# Set of occuring phonemes to iterate on when creating dictionary
#set_phon = set(prepare_data.read_testfiles()[::2])
set_phon = set(pd_LSR.read_testfiles()[::3])
#print(set_phon)

# A list of phonemes in occuring order in the actual and pred lists
#a_phone_list = prepare_data.read_testfiles()[::2]
a_phone_list = pd_LSR.read_testfiles()[::3]
#print(a_phone_list)

# Use list comprehension to interweave the phoneme list with the list of predicted durations
#   so we can create the dictionary of predictions per phoneme
pred_list = [x for y in zip (a_phone_list, predictions) for x in y]


# Dictionary of actual values per phoneme
a_dict = defaultdict(list)
# Dictionary of predicted values per phoneme
p_dict = defaultdict(list)


# Populate dictionary of actual values
for el in set_phon:
	i = 0
	for y in testlist:
		if el == y:
			a_dict[el].append(testlist[i+1])
		i += 1
#print(a_dict)
# Populate dictionary of predicted values
for el in set_phon:
	j = 0
	for z in pred_list:
		if el == z:
			p_dict[el].append(pred_list[j+1])
		j += 1
#print(p_dict)
# Create lists for grouping rmse results
b_list = []
w_list = []
# Populate b_list with all phonemes having a better score than global rmse
# 	and w_list with all phonemes scoring worse than global rmse.
for el in set_phon:
	rmse = performance_measures.calc_error_for_data(p_dict[el], a_dict[el])
	if rmse[0] <= global_rmse:
		b_list.append(el)
	else:
		print(el + ": " + str(round(rmse[0], 4)) + "  " + str(round(rmse[1], 4)))
		w_list.append(el)
print("Scored better: " + str(b_list))
print("Scored worse: " + str(w_list))