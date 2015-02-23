#!/usr/bin/env python
# coding: utf-8
# Simple translator for a culled corpus

import pprint
import itertools as it
import re
import ourdict
from nlp_tools import Tokenizer, Tagger, Stemmer
from LaplaceBigramLanguageModel import LaplaceBigramLanguageModel
from ourdict import Dict

class Translator:
	
	def __init__(self):
		self.dictionary = Dict()
		# self.word_bigram_model = LaplaceBigramLanguageModel

	def translate_sentence(self, sentence):
		words = []
		words = re.split('[^\wñáéíóúÁÉÍÓÚ]', sentence)
		d = ourdict.Dict()
		for word in words:
			if (word):
				word = word.lower()
				e_word = d.dictionary[word][0]

	def best_cand(self, cands, punct, index, preword):
		best = ""
		top_score = 0.0
		for cand in cands:
			bigram = "%s-%s" % (preword, cand)
			score = self.word_bigram_model.word_bigramCounts[bigram]
			if (score > top_score):
				best = cand
				top_score = score
		return best

	#corpus
	def use_word_bigram(self, sentence):
		words = sentence.split()
		e_translate = self.dictionary.dictionary[(words[0]).lower()][0] + " "
		for i in range(1, len(words)):
			word = words[i]
			# print "word is %s" % word
			punct = ""
			if ',' in word or '.' in word:
				punct = word[len(word) - 1]
				word = word[:-1]
				# print "new word: %s" % word
			cands = self.dictionary.dictionary[word]
			e_translate += self.best_cand(cands, punct, i, e_translate.split()[i - 1])
			if (punct):
				e_translate += punct
			e_translate += " "
			# return self.best_cand(cands, punct, i, words[i - 1])
		print "original sentence: %s" % sentence
		print "translated sentence: %s" % e_translate 

	# def remove_parens(self, sentence):
	# 	final = ""
	# 	for word in sentence:
	# 		if word[0] != "(":
	# 			final += word + " "
	# 	return final

	#bigram classifier
	def build_bigram(self, corpus):
		f = open(corpus)
		self.word_bigram_model = LaplaceBigramLanguageModel(f)	


	# print re.split('[^\wñáéíóúÁÉÍÓÚ]',"Cuando se accede al ordenador como tal, pueden añadirse otros usuarios, configurar Usuarios Múltiples de Mac OS X, cambiar determinados ajustes del sistema y, en general, disponer de mayor acceso al sistema.")

def main():
    """Tests the model on the command line. This won't be called in
        scoring, so if you change anything here it should only be code
        that you use in testing the behavior of the model."""
    
    tranny = Translator()
    tranny.translate_sentence("Cuando se accede al ordenador como tal, pueden añadirse otros usuarios, configurar Usuarios Múltiples de Mac OS X, cambiar determinados ajustes del sistema y, en general, disponer de mayor acceso al sistema.")
    tranny.build_bigram('giddycorpus.txt')
    tranny.use_word_bigram("Cuando accede al ordenador como un administrador, pueden añadirse otros usuarios, configurar")

if __name__ == '__main__':
    main()