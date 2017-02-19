import error
import prepare_data
import numpy as np

phon_dict, test_dict, tm_dict = prepare_data.calculate_pho_mean(prepare_data.read_trainig_files())
#print(test_dict)

testlist = prepare_data.read_testfiles()
trainingdict = tm_dict

predictions = prepare_data.create_prediction_list(testlist, trainingdict)
actual = prepare_data.read_testfiles()[1::2]

#print(predictions)
#print(prepare_data.read_testfiles())
#print(actual)

rmse, mae = error.calc_error_for_data(predictions, actual)
print(rmse, mae)