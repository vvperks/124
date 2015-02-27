# $ pip install nltk
# $ python
# >>> import nltk
# >>> nltk.download('all')  // you can be more specific than this, but w/e

'''Usage:

sentence = 'Hola, como estas?'

from nlp_tools import *

tokenizer = Tokenizer()
tagger = Tagger()
stemmer = Stemmer()

tokens = tokenizer.tokenize(sentence)
tags = tagger.tag(tokens)
stems = stemmer.stem(tokens)
'''

from nltk import word_tokenize
import pickle
import os.path

##################### TOKENIZATION #########################
class Tokenizer:
	def __init__(self):
		self.tokenizer = word_tokenize
	def tokenize(self, sentence):
		return self.tokenizer(sentence)

##################### POS TAGGING #######################
class Tagger:
	def __init__(self):
		if os.path.exists('tagger_spanish.pickle'):
			with open('tagger_spanish.pickle', 'r') as file_obj:
			    self.tagger = pickle.load(file_obj)
		else:
			print 'tagger_spanish.pickle not found. Training tagger... may take a few minutes...'
			from nltk import UnigramTagger, BigramTagger, TrigramTagger
			from nltk.corpus import cess_esp
			sents = cess_esp.tagged_sents()
			unigram_tagger = UnigramTagger(sents)
			bigram_tagger = BigramTagger(sents, backoff=unigram_tagger) # uses unigram tagger in case it can't tag a word
			self.tagger = unigram_tagger
			with open('tagger_spanish.pickle', 'w') as file_obj:
			    pickle.dump(self.tagger, file_obj)		# Dump trained tagger
	def tag(self, tokens):
		return self.tagger.tag(tokens)

##################### STEMMING ########################
class Stemmer:
	def __init__(self):
		from nltk.stem.snowball import SnowballStemmer
		self.stemmer = SnowballStemmer("spanish")
	def stem(self, tokens):
		return [self.stemmer.stem(token) for token in tokens]

#############################################################

