from nltk.stem.snowball import SnowballStemmer
from nltk import WordNetLemmatizer
from nltk import word_tokenize
import re
from os import listdir

stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords

remove = ['~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', '|', '\\', ':', '"', "'", '<', '>', '/']

def preprocess_text(text) :
	text = text
	for r in remove :
		text = text.replace(r, ' ')
	text = re.sub(r'([\.\?\!,;])(\D)', r' \1 \2', text)
	return text

def norm(word, low=True, lem=True, stem=True) :
	if low :
		word = word.lower()
	if lem :
		word = lemmatizer.lemmatize(word)
	if stem :
		word = stemmer.stem(word)
	return word

def import_stopwords() :
	return stopwords.words("english")

stopwords = import_stopwords()

def get_tokens_from_text(line, low=True, lem=True, stem=True) :
	text = preprocess_text(line)
	tokens = word_tokenize(text)
	tokens = [norm(t, low, lem, stem) for t in tokens if t.lower() not in stopwords and len(t) > 2]
	return tokens

def get_tokens_from_file(file_name, low=True, lem=True, stem=True) :
	tokens = get_tokens_from_text(open(file_name).read().decode('utf-8'), low, lem, stem)
	print('Done ' + file_name)
	return tokens

def get_tokens_over_paths(paths, low=True, lem=True, stem=True) :
	tokens = []
	for p in paths :
		for f in listdir(p) :
			tokens += get_tokens_from_file(p+f, low, lem, stem)
	return tokens
