import numpy as np

predictions = [0.06, 0.06, 0.06, 0.06]
actual_values = [0.04, 0.06, 0.02, 0.06]

def rmse(prediction, actual):
	return np.sqrt(((prediction - actual) ** 2).mean())

rmse_val = rmse(np.array(predictions), np.array(actual_values))

def mae(prediction, actual):
	return np.absolute(prediction - actual).mean()

mae_val = mae(np.array(predictions), np.array(actual_values))

#print(str(rmse_val))
#print(str(mae_val))