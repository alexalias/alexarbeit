import re
import model_utilities
import model_wl
import model_wl_ip
import model_wl_ipdur
import model_ipdur


# List of paths to the files in our test data, to later iterate on
#path_list_test = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Test')

valid_phonemes = ["a", "a~", "e", "E", "I", "i", "O", "o", "U", "u", "Y", "y", "9", "2", "a:", "a~:", "e:", "E:", "i:",
                 "o:", "u:", "y:", "2:", "OY", "aU", "aI", "@", "6", "z", "S", "Z", "C", "x", "N", "Q", "b", "d", "f", 
                 "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v"]

# Model type uses individual phonemes and their median, mean, or both in words having specific no. of phonemes
# Actually creates the lists of predictions and actual values to evaluate model
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
# Return: 2 lists of integers
def create_modelIPdur_lists(model):
	predictions_list, actuals_list = [], []
	for datei in path_list_test:
		work_file = open(datei)
		for line in work_file:
			# Restrain model to relevant phonemes
			if re.match("MAU", line) and (str(line.split()[4]) in valid_phonemes):
				predicted_pdur = model_ipdur.pdur_prediction_value(datei, int(line.split()[3]), str(line.split()[4]), model)
				predictions_list.append(predicted_pdur)

				actuals_list.append(int(line.split()[2]))
		work_file.close()
	#print(len(predictions_list))
	#print(len(actuals_list))
	return predictions_list, actuals_list

# Model type uses individual phonemes and their median, mean, or both
# Actually creates the lists of predictions and actual values to evaluate model
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
# Return: 2 lists of integers
def create_modelWLIP_lists(model, path_list_test, path_list_training):
	predictions_list, actuals_list = [], []
	for datei in path_list_test:
		work_file = open(datei)
		for line in work_file:
			# Restrain model to relevant phonemes
			if re.match("MAU", line) and (str(line.split()[4]) in valid_phonemes):
				predicted_pdur = model_wl_ip.pdur_prediction_value(datei, int(line.split()[3]), str(line.split()[4]), model, path_list_training)
				predictions_list.append(predicted_pdur)

				actuals_list.append(int(line.split()[2]))
		work_file.close()
	return predictions_list, actuals_list
#print(create_modelWLIP_lists(0)[0])

# Model type uses individual phonemes and their median, mean, or both in words having specific no. of phonemes
# Actually creates the lists of predictions and actual values to evaluate model
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
# Return: 2 lists of integers
def create_modelWLIPdur_lists(model):
	predictions_list, actuals_list = [], []
	for datei in path_list_test:
		work_file = open(datei)
		for line in work_file:
			# Restrain model to relevant phonemes
			if re.match("MAU", line) and (str(line.split()[4]) in valid_phonemes):
				predicted_pdur = model_wl_ipdur.pdur_prediction_value(datei, int(line.split()[3]), str(line.split()[4]), model)
				predictions_list.append(predicted_pdur)

				actuals_list.append(int(line.split()[2]))
		work_file.close()
	return predictions_list, actuals_list

# Model type uses phoneme-classes and their median, mean, or both
# Actually creates the lists of predictions and actual values to evaluate model
# @param model: 0, 1, or 2 meaning (median, mean, or (median + mean)/2)
# Return: 2 lists of integers
def create_modelWL_lists(model):
	predictions_list, actuals_list = [], []
	for datei in path_list_test:
		work_file = open(datei)
		for line in work_file:
			# Restrain model to relevant phonemes
			if re.match("MAU", line) and (str(line.split()[4]) in valid_phonemes):
				predicted_pdur = model_wl.pdur_prediction_value(datei, int(line.split()[3]), str(line.split()[4]), model)
				predictions_list.append(predicted_pdur)

				actuals_list.append(int(line.split()[2]))
		work_file.close()
	return predictions_list, actuals_list

#predictions_list = create_pred_act_lists(0)[0]#, actuals_list = create_pred_act_lists(0)