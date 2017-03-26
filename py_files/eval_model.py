import performance_measures
import numpy as np
import create_eval_lists

# Create the two lists of values to be compared
predictions_list1 = create_eval_lists.create_modelWL_lists(0)[0]
actuals_list1 = create_eval_lists.create_modelWL_lists(0)[1]


predictions_list2 = create_eval_lists.create_modelWLIP_lists(0)[0]
actuals_list2 = create_eval_lists.create_modelWLIP_lists(0)[1]
#print(predictions_list)
#print(actuals_list)

evaluation_lists = [(predictions_list1, actuals_list1), (predictions_list2, actuals_list2)]

# Evaluate model with: RMSE, MAE, and Pearson's correlation coefficient
global_rmse, mae = performance_measures.calc_error_for_data(predictions_list2, actuals_list2)
corrCoef = performance_measures.corrCoef(predictions_list2, actuals_list2)[0]
print(global_rmse, mae, corrCoef)

#print(predictions_list[:5])
#print(actuals_list[:5])

