import performance_measures
import numpy as np
import create_eval_lists
import model_utilities
import time

#### Running this file prints out the results of the performance evaluation of the differen models ####

# Create the two lists of values to be compared, for each model a pair
 # - 1st numeric parameter allows chosing the unit on which one evaluates the model (0 = median, 1 = mean, 2 = (median + mean)/2 )
 # - 2nd numeric parameter should not be changed (it's just the indices of the elem in the result vector to be used)

# Splitting dataset 10 times into disjunct training- and test-datasets (90% to 10%)
rmse_list, mae_list, corr_list = [], [], []

dataset = model_utilities.get_path_list('C:/Users/alexutza_a/Abschlussarbeit/DB_Verbmobil/Evaluation/Training')

global_rmse, mae = performance_measures.calc_error_for_data(create_eval_lists.create_modelIPdur_lists(1)[0], create_eval_lists.create_modelIPdur_lists(1)[1])
corrCoef = performance_measures.corrCoef(create_eval_lists.create_modelIPdur_lists(1)[0], create_eval_lists.create_modelIPdur_lists(1)[1])[0]

print(global_rmse, mae)
print(corrCoef)