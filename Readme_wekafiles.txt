##### Weka file info ######

dataset files 
##############

cart_58db_SR.arff >> database-file used to create the M5P and REPTree models
		  >> contains 58% of the whole Verbmobil phonemic data

cart_testAKX.arff >> file with unseen testdata obtained from one speaker (AKX)

cart_min_trainAKX.arff >> file containing training data obtained from only one speaker in VM-II (AKX).
		       >> it includes phoneme related information from 168 speech turns.

cart_min_testAKX.arff >> file containing test data obtained from only one speaker in VM-II (AKX).
		       >> it includes phoneme related information from 17 speech turns.

Beside *.arff files, the folder "wekadateien" contains a set of text files and a set of modelfiles:
##################################################################################################
Model files: models created from our database, which may be loaded into Weka and further analysed.
Text files: result buffer of the tested models on different database konfigurations.

Naming convention: <model_name>_<dataset>SR(with speech rate)/_noSR(without speech rate)_[test set used, if case]_result/model.<ext>
E.g.
----
M5P_58dbSR_testAKX_result.txt >> Result of the test of M5P model, trained with the cart_58db_SR.arff database file
				and tested on the cart_testAKX.arff db-file.
		   
REPTree_58db_noSR_result.txt >> Result of the test of REPTree model, trained and tested on the cart_58db_SR.arff database file
				and after eliminating the speech rate feature.

M5P_minAKX_SR_result.txt       -> using the min_trainAKX file for training and min_testAKX file for testing
REPTree_minAKX_SR_result.txt   -> using the min_trainAKX file for training and min_testAKX file for testing