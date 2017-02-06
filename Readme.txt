DATA PROCESSING

File description:

arff_file_builder.py -> fetches all data needed for data mining with weka in a single text file.

phon_dict.py -> creates a dictionary of a given list of phonemes (key) and their related attributes (values) in Verbmobil.
Attributes: 
	- Phoneme: name of the phoneme, just to make things easier later
	- Filename: name of the file in which the specific phoneme duration occurs 
	- Position in Speech: Start, Middle, End
	- Word: word or type of word in which the specific phoneme duration occurs
	- Pause: if a pause preceedes or follows the word in which the specific phoneme duration occurs, no initial or final pauses considered
	- Stress: specifically for vowels, uses the KAN tier to check what type of stress that vowel has (p_stress, s_stress, none)
	- Overlapping (overlapped, no overlapping): if the word of occurence overlaps with somebody else's speech
	- Speech rate: number of phonemes/total duration of speech without pauses per file
	- Local speech rate: a combination of phone rate and syllable rate per word_duration in sec
	- Speech rate: number of realized syllables/total duration of speech without pauses per file
	- Speech rate: number of planed syllables /total duration of speech without pauses per file
	- Duration: the phoneme duration marked in the MAU tier

stress.py -> sets the stress label for the given phoneme key
	> works for diphthongs, long vowels and schwa
	> for the other vowels I still have to fix the problem of dropped vowels, when I compare the MAU annotation against the KAN annotation

speech_rate.py -> calculates the different speech rates

old_dict.py -> not used anymore
creates a dictionary that associates the duration dictionary to a specific phoneme (key), together with other statistical data regarding the duration of that specific phoneme.
Values (attributes of the phoneme):
	- Duration dictionary: see duration_dict for description
	- Mininum length of that phoneme
	- Maximum length of that phoneme
	- Median of phoneme lengths for given phoneme
	- Mean of phoneme lengths for given phoneme
	- Mode of phoneme lengths for given phoneme
	- Standard deviation for given phoneme lengths
	- Length interval for given phoneme