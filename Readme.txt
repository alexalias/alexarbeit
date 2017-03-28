
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

- eval_model.py : run this file to evaluate given models
	- performance_measures.py: contains the code to calculate the RMSE, MAE, and Pearson correlation coefficient.

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

 Exploring the data 
####################

arff_file_builder.py -> fetches all data from phon_dict.py for data mining with weka in a single text file.

phon_dict.py:   - creates a dictionary of a given list of phonemes (key) and their related attributes (values) in Verbmobil.
		- use the varible "path_list" defined at beginning of file to provide the link to the needed database
Attributes: 
	- Phoneme: name of the phoneme, just to make things easier later
	- Filename: name of the file in which the specific phoneme duration occurs 
	- Position in Speech: Start, Middle, End
	- Word: word or type of word in which the specific phoneme duration occurs
	- Pause: if a pause preceedes or follows the word in which the specific phoneme duration occurs, no initial or final pauses considered
	- Stress: specifically for vowels, uses the KAN tier to check what type of stress that vowel has (p_stress, s_stress, none)
	- Overlapping (overlapped, no overlapping): if the word of occurence overlaps with somebody else's speech
	- Speech rate: number of phonemes/total duration of speech without pauses per file
	############# commented out ###- Local speech rate: a combination of phone rate and syllable rate per word_duration in sec
	- Speech rate: number of realized syllables/total duration of speech without pauses per file
	- Speech rate: word duration (sec) / no. of phonemes
	### only for Q ### default state: commented out: position (it can be only word-initial or morpheme-initial)
	- Syllable position in word: one_s = one-syllable-word, w_1 = initial syllable, w_2 = middle syllable, w_3 = final syllable
	- Duration: the phoneme duration marked in the MAU tier (in samples)

stress.py -> sets the stress label for the given phoneme key; used in phon_dict
	  -> works for diphthongs, vowels and schwa
	  -> consonants should actually be categorized based on stress type of nearby vowels, but not implemented

speech_rate.py -> calculates different types of speech rates

find_syl_position.py -> used in phon_dict to get the syllable postition in word

old_dict.py -> not used anymore
creates a dictionary that associates the duration dictionary to a specific phoneme (key), 
together with other statistical data regarding the duration of that specific phoneme.
Values (attributes of the phoneme):
	- Duration dictionary: see duration_dict for description
	- Mininum length of that phoneme
	- Maximum length of that phoneme
	- Median of phoneme lengths for given phoneme
	- Mean of phoneme lengths for given phoneme
	- Mode of phoneme lengths for given phoneme
	- Standard deviation for given phoneme lengths
	- Length interval for given phoneme

Other files: help functions used previousely but of no great importance.