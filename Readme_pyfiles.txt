Before running python notebooks: you need to add the py_files folder to the pythonpath (export PYTHONPATH=py_files).
Some functions only work for the subgroup of files in our dataset til g371acn1.

 Build and evaluate models:
############################

Overview:
									    performance_measures
		     -> model_ipdur  -					    	    |
		   /			\					    V
 model_utilities -   -> model_wl_ip  -	  -->	create_eval_lists    ------->	eval_model
		   \			/
		     ->	model_wl     -

File description:
Use the dataset_path variable at the beginning of each file to point to the dataset you want to use (link contained in string).

- eval_model.py : run this file to evaluate given models. As only model_wl_ipdur is being handled in the paper, the file
	is organized to evaluate only this model.
	- performance_measures.py: contains the code to calculate the RMSE, MAE, and Pearson correlation coefficient.

### Present configuration of eval_model.py (and correlated files) evaluates only model_wl_ip. Use the var "dataset" ###
######### to provide a link to the dataset. Split into training- and test-dataset is done afterwards using ############
############################################# 10-fold cross-validation ################################################


- create_eval_lists.py : - gets the prediction- and actual-lists from different models.
			 - contains a set of almost identical functions (one per model)
			 - use the first line of code after imports to provide the path to the test-dataset (var "path_list...")

Models:
-----> use the first line of code in each model after imports to provide the path to the training-dataset (var "path_list...") <----------

- model_ipdur (baseline): the predicted duration of each phoneme is its mean duration from the training dataset
- model_wl_ip : - the predicted duration of each phoneme represents a quotient of the word duration it is contained in
		- to calculate the quotient we define "word_length" as number of phonemes in word
		- the quotient is then calculated as mean of shares that phoneme has in words of word_length = x, in training data
- model_wl: - similar as model_wl_ip, using classes of phonemes instead of individual phonemes 
		(challenge in finding an appropriate clustering of phonemes to define classes)

- model_utilities: a set of help functions to use in models
		(e.g. hier we get the list of paths to the files of the needed dataset to iterate on)


Files for Exploring the data 
############################

new_arff_file_builder.py -> fetches all data from new_phon_dict.py for data mining with weka in a single text file.
			-> After txt-file is created, you need to place a comma between t and v at the end of the value list of 
			   the firs attribute. Then save as *.arff file and load into Weka.

new_phon_dict.py:   - creates a dictionary of a given list of phonemes (key) and their related attributes (values) in Verbmobil.
		- use the varible "path_list" defined at beginning of file to provide the link to the needed database

stress.py -> sets the stress label for the given phoneme key; used in phon_dict
	  -> works for diphthongs, vowels and schwa
	  -> consonants are being categorized based on stress type of nearby vowels, not implemented, as not needed

new_SR.py -> calculates different types of speech rates

get_syllables.py -> used in phon_dict to get the syllable postition in word

t_modify_files.py -> used to annotate syllable and stress information
Other files: help functions used but of no great importance.