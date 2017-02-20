import error
import prepare_data
import numpy as np
from collections import defaultdict

phon_dict, test_dict, tm_dict = prepare_data.calculate_pho_mean(prepare_data.read_trainig_files())
#print(test_dict)

testlist = prepare_data.read_testfiles()
trainingdict = test_dict

predictions = prepare_data.create_prediction_list(testlist, trainingdict)
actual = prepare_data.read_testfiles()[1::2]

#print(predictions)
#print(prepare_data.read_testfiles())
#print(actual)

global_rmse, mae = error.calc_error_for_data(predictions, actual)
print(global_rmse, mae)


### Following is rmse calculation individually (per phoneme) ###



# Set of occuring phonemes to iterate on when creating dictionary
set_phon = set(prepare_data.read_testfiles()[::2])
# A list of phonemes in occuring order in the actual and pred lists
a_phone_list = prepare_data.read_testfiles()[::2]
# Use list comprehension to inweave the phoneme list with the list of predicted durations
#   so we can create the dictionary of predictions per phoneme
pred_list = [x for y in zip (a_phone_list, predictions) for x in y]

# Dictionary of actual values per phoneme
a_dict = defaultdict(list)
# Dictionary of predicted values per phoneme
p_dict = defaultdict(list)

# Populate dictionary of actual values
for el in set_phon:
	for y in testlist:
		if el == y:
			a_dict[el].append(testlist[testlist.index(y)+1])

# Populate dictionary of predicted values
for el in set_phon:
	for z in pred_list:
		if el == z:
			p_dict[el].append(pred_list[pred_list.index(z)+1])

# Create lists for grouping rmse results
b_list = []
w_list = []
# Populate b_list with all phonemes having a better score than global rmse
# 	and w_list with all phonemes scoring worse than global rmse.
for el in set_phon:
	rmse = error.calc_error_for_data(p_dict[el], a_dict[el])
	if rmse[0] <= global_rmse:
		b_list.append(el)
	else:
		print(el + ": " + str(rmse))
		w_list.append(el)
print("Scored better: " + str(b_list))
print("Scored worse: " + str(w_list))