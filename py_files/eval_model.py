import performance_measures
import numpy as np
import create_eval_lists

# Create the two lists of values to be compared
predictions_list1 = create_eval_lists.create_modelWL_lists(0)[0]
actuals_list1 = create_eval_lists.create_modelWL_lists(0)[1]


predictions_list2 = create_eval_lists.create_modelWLIP_lists(2)[0]
actuals_list2 = create_eval_lists.create_modelWLIP_lists(2)[1]
#print(predictions_list)
#print(actuals_list)

predictions_list3 = create_eval_lists.create_modelIPdur_lists(2)[0]
actuals_list3 = create_eval_lists.create_modelIPdur_lists(2)[1]

model_name_list = ["WL", "WL_IP", "IP_dur"]
evaluation_lists = [(predictions_list1, actuals_list1), (predictions_list2, actuals_list2), (predictions_list3, actuals_list3)]

# Evaluate models with: RMSE, MAE, and Pearson's correlation coefficient
for i in range(len(evaluation_lists)):
	global_rmse, mae = performance_measures.calc_error_for_data(evaluation_lists[i][0], evaluation_lists[i][1])
	corrCoef = performance_measures.corrCoef(evaluation_lists[i][0], evaluation_lists[i][1])[0]
	print("RMSE for the" + model_name_list[i] + "-model: " + str(global_rmse))
	print("MAE for the" + model_name_list[i] + "-model: " + str(mae))
	print("Pearson corrCoef for the " + model_name_list[i] + "-model: "  + str(corrCoef))