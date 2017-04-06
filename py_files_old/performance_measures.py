import numpy as np
from scipy.stats.stats import pearsonr

#predictions = [0.06, 0.06, 0.06, 0.06]
#actual_values = [0.04, 0.06, 0.02, 0.06]

# Returns the list of predicted values, for the training set
def get_predictions(predictions_dict):
	predictions = []
	for key in predictions_dict.keys():
		for i in range(1, len(predictions_dict[key])):
			predictions.append(predictions_dict[key][0])
	#	if key in vowel_list:
	#		for i in range(1, len(durations_dict[key])):
	#			predictions.append(1149)
	#	else:
	#		for i in range(1, len(durations_dict[key])):
	#			predictions.append(durations_dict[key][0])
	#print(durations_dict)
	#print(predictions)

	return predictions

# Returns the list of actual values, for the training set
def get_observed(observed_dict):
	observed = []

	for key in observed_dict.keys():
		observed += observed_dict[key]
	#print(observed)
	return observed
# Need
def RMSE(prediction, actual):
	return np.sqrt(((prediction - actual) ** 2).mean())


# Need
def MAE(prediction, actual):
	return np.absolute(prediction - actual).mean()

def corrCoef(prediction, actual):
	return pearsonr(np.array(prediction), np.array(actual))

#rmse_val = rmse(np.array(predictions), np.array(actual_values))
#mae_val = mae(np.array(predictions), np.array(actual_values))

# Need
# Compares the two lists via rmse and mae.
def calc_error_for_data(predictions, actuals):
	rmse = RMSE(np.array(predictions), np.array(actuals))
	rmse *= 0.0000625
	mae = MAE(np.array(predictions), np.array(actuals))
	mae *= 0.0000625

	return rmse, mae