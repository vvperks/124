#!/usr/bin/env python
# coding: utf-8
# Simple translator for a culled corpus

import re
import ourdict
from LaplaceBigramLanguageModel import LaplaceBigramLanguageModel
from nlp_tools import Tokenizer

import parse

class Translator:
	
	def __init__(self, bigram_count_file_name):
		self.dictionary = ourdict.dictionary
		self.tokenizer = Tokenizer()
		with open(bigram_count_file_name, 'r') as f:
			self.bigram_model = LaplaceBigramLanguageModel(f)

	def translate_sentence(self, sentence):
		###################################################################################
		# Call PRE-processing rules as functions of sentence and returning sentences HERE #
		###################################################################################
		tokens = self.tokenizer.tokenize(sentence)
		###############################################################
		# or as functions of token list and returning toke list HERE. #
		###############################################################
		translated_tokens = ['^'] # Arbitrary start token
		for token in tokens:
			token = token.lower()
			translated_tokens.append(self.find_next_word(token, translated_tokens))
		#######################################################################################
		# Call POST-processing rules as functions of token list and returning token list HERE #
		#######################################################################################	
		translation = self.format(translated_tokens)
		###########################################################
		# or as functions of sentence and returning sentence HERE #
		###########################################################
		print "***ORIGINAL SENTENCE***: %s" % sentence
		print "***OUR TRANSLATION***: %s" % translation
		return translation

	def find_next_word(self, word, current_translation):
		candidate_words = self.dictionary[word]
		top_score = float("-inf")
		prev_word = current_translation[-1]
		if (prev_word == ',') or (prev_word == '.'):
			prev_word = current_translation[-2] 	# If the previous token is punctuation, get what's before it
		for word in candidate_words:
			score = self.bigram_model.score([prev_word, word])
			if (score > top_score):
				best = word
				top_score = score
		return best

	def format(self, token_list):
		''' takes the list of translated words and formats it nicely for printing '''
		s = " ".join(token_list[1:])	# Remove the leading start token and turn into a spaced string
		s = re.sub(r' ([\.,])', r'\1', s)	# Remove whitespace before punctuation
		s = s[0].upper() + s[1:]		# Capitalize the sentence
		return s

	###########################################################
	# ADD YOUR PREPROCESSING + POSTPROCESSING FUNCTIONS HERE. #
	###########################################################

def main():
    """Tests the model on the command line. This won't be called in
        scoring, so if you change anything here it should only be code
        that you use in testing the behavior of the model."""
    
    tranny = Translator('giddycorpus.txt')
    tranny.translate_sentence("Cuando se accede al ordenador como tal, pueden añadirse otros usuarios, configurar Usuarios Múltiples de Mac OS X, cambiar determinados ajustes del sistema y, en general, disponer de mayor acceso al sistema.")
    for i, (spanish_sentence, english_sentence) in enumerate(zip(ourdict.spanish_sentences, ourdict.english_sentences)):
    	translation = tranny.translate_sentence(spanish_sentence)
    	print "number: %d" % i
    	print "***ACTUAL TRANSLATION***: %s" % english_sentence
    	print " "


if __name__ == '__main__':
    main()
