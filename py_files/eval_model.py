import performance_measures
import numpy as np
import create_eval_lists
import model_utilities
import time

#### Running this file prints out the results of the performance evaluation of the differen models ####

# Create the two lists of values to be compared, for each model a pair
 # - 1st numeric parameter allows chosing the unit on which one evaluates the model (0 = median, 1 = mean, 2 = (median + mean)/2 )
 # - 2nd numeric parameter should not be changed (it's just the indices of the elem in the result vector to be used)
#evaluation_lists_initial = [(create_eval_lists.create_modelWL_lists(1)[0], create_eval_lists.create_modelWL_lists(1)[1]), 
#					(create_eval_lists.create_modelWLIP_lists(1)[0], create_eval_lists.create_modelWLIP_lists(1)[1]), 
#					(create_eval_lists.create_modelIPdur_lists(1)[0], create_eval_lists.create_modelIPdur_lists(1)[1])]

# Splitting dataset 10 times into disjunct training- and test-datasets (90% to 10%)
rmse_list, mae_list, corr_list = [], [], []


dataset = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training')
num_folds = 10
subset_size = int(len(dataset)/num_folds)
for i in range(num_folds):
	t1 = time.time()
	path_list_test = dataset[i*subset_size:][:subset_size]
	path_list_training = dataset[:i*subset_size] + dataset[(i+1)*subset_size:]

	# Taking the best model for further testing
	evaluation_lists = [(create_eval_lists.create_modelWLIP_lists(1, path_list_test, path_list_training)[0], 
		create_eval_lists.create_modelWLIP_lists(1, path_list_test, path_list_training)[1])]

	for i in range(len(evaluation_lists)):
		global_rmse, mae = performance_measures.calc_error_for_data(evaluation_lists[i][0], evaluation_lists[i][1])
		corrCoef = performance_measures.corrCoef(evaluation_lists[i][0], evaluation_lists[i][1])[0]
	rmse_list.append(global_rmse)
	mae_list.append(mae)
	corr_list.append(corrCoef)
	print(str(i) + ". fold time:" + str(time.time() - t1))
# A name list to use when printing the results
model_name_list = ["WL", "WL_IP", "IP_dur"]

# Average of the 10-fold cross-validation run
print("Average RMSE of the KFold: " + round(np.mean(rmse_list), 4))
print("Average MAE of the KFold: " + round(np.mean(mae_list), 4))
print("Average corrCoef of the KFold: " + round(np.mean(corr_list), 4))

# Evaluate models with: RMSE, MAE, and Pearson's correlation coefficient
#for i in range(len(evaluation_lists)):
#	global_rmse, mae = performance_measures.calc_error_for_data(evaluation_lists[i][0], evaluation_lists[i][1])
#	corrCoef = performance_measures.corrCoef(evaluation_lists[i][0], evaluation_lists[i][1])[0]
#	print("RMSE for the" + model_name_list[i] + "-model: " + str(global_rmse))
#	print("MAE for the" + model_name_list[i] + "-model: " + str(mae))
#	print("Pearson corrCoef for the " + model_name_list[i] + "-model: "  + str(corrCoef) + "\n")