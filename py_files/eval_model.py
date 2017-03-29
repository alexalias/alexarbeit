import performance_measures
import numpy as np
import create_eval_lists

#### Running this file prints out the results of the performance evaluation of the differen models ####

# Create the two lists of values to be compared, for each model a pair
 # - 1st numeric parameter allows chosing the unit on which one evaluates the model (0 = median, 1 = mean, 2 = (median + mean)/2 )
 # - 2nd numeric parameter should not be changed (it's just the indices of the elem in the result vector to be used)
evaluation_lists = [(create_eval_lists.create_modelWL_lists(1)[0], create_eval_lists.create_modelWL_lists(1)[1]), 
					(create_eval_lists.create_modelWLIP_lists(1)[0], create_eval_lists.create_modelWLIP_lists(1)[1]), 
					(create_eval_lists.create_modelIPdur_lists(1)[0], create_eval_lists.create_modelIPdur_lists(1)[1])]

# A name list to use when printing the results
model_name_list = ["WL", "WL_IP", "IP_dur"]

# Evaluate models with: RMSE, MAE, and Pearson's correlation coefficient
for i in range(len(evaluation_lists)):
	global_rmse, mae = performance_measures.calc_error_for_data(evaluation_lists[i][0], evaluation_lists[i][1])
	corrCoef = performance_measures.corrCoef(evaluation_lists[i][0], evaluation_lists[i][1])[0]
	print("RMSE for the" + model_name_list[i] + "-model: " + str(global_rmse))
	print("MAE for the" + model_name_list[i] + "-model: " + str(mae))
	print("Pearson corrCoef for the " + model_name_list[i] + "-model: "  + str(corrCoef) + "\n")