import error
import fetch_data
import numpy as np

durations_dict = fetch_data.calculate_pho_mean(fetch_data.read_trainig_files())
st_value_means = fetch_data.standard_value_means()

def get_predictions():
	predictions = []
	for key in durations_dict.keys():
		for i in range(1, len(durations_dict[key])):
			predictions.append(durations_dict[key][0])

	#print(durations_dict)
	#print(predictions)

	return predictions

def get_observed():
	observed = []

	for key in durations_dict.keys():
		observed += durations_dict[key][1:]
	#print(observed)
	return observed

def calc_rmse_for_trdata():
	min_o = min(get_observed())
	max_o = max(get_observed())
	rmse = error.rmse(np.array(get_predictions()), np.array(get_observed()))
	rmse /= (max_o - min_o)
	mae = error.mae(np.array(get_predictions()), np.array(get_observed()))
	
	return rmse, mae

print(calc_rmse_for_trdata())