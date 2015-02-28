#!/usr/bin/env python
# coding: utf-8
# Simple translator for a culled corpus

import re
import ourdict
from LaplaceBigramLanguageModel import LaplaceBigramModel
from unigram_model import LaplaceUnigramModel
from nlp_tools import Tokenizer
import parse

class Translator:
	
	def __init__(self, bigram_count_file_name, bigram_model_pickle='bigram_model.pickle'):
		self.dictionary = ourdict.dictionary
		self.tokenizer = Tokenizer()
		with open(bigram_count_file_name, 'r') as f:
			self.bigram_model = LaplaceBigramModel(f)
		with open('windows1.txt', 'r') as f:
			self.unigram_model = LaplaceUnigramModel(f)

	def translate_sentence(self, sentence):
		###################################################################################
		# Call PRE-processing rules as functions of sentence and returning sentences HERE #
		###################################################################################
		tokens = self.tokenizer.tokenize(sentence)
		###############################################################
		# or as functions of token list and returning toke list HERE. #
		tokens = self.remove_se(tokens)
		###############################################################
		translated_tokens = ['^'] # Arbitrary start 
		for i in range(0, len(tokens)):
			token = tokens[i].lower()
			if (token == "para"):
				translated_tokens.append(self.para_process(token, tokens[i + 1]))
			else:
				translated_tokens.append(self.find_next_word(token, translated_tokens))

		# for token in tokens:
		# 	token = token.lower()
		# 	translated_tokens.append(self.find_next_word(token, translated_tokens))
		#######################################################################################
		# Call POST-processing rules as functions of token list and returning token list HERE #
		#######################################################################################	
		translation = self.format(translated_tokens)
		###########################################################
		# or as functions of sentence and returning sentence HERE #
		translation = self.reverse_noun_adj([translation])		  #
		###########################################################
		return translation

	def para_process(self, para, next_word):
		if (len(next_word) > 1):
			suffix = next_word[len(next_word)-2:]
			print "suffix: %s" % suffix
			if suffix == 'ar' or suffix == 'er' or suffix == 'ir':
				return 'to'
			else:
				return 'for'
		return 'for'

	def find_next_word(self, word, current_translation):
		candidate_words = self.dictionary[word]
		top_score = float("-inf")
		prev_word = current_translation[-1]
		if (prev_word == ',') or (prev_word == '.'):
			prev_word = current_translation[-2] 	# If the previous token is punctuation, get what's before it
		for word in candidate_words:
			# score = self.bigram_model.score([prev_word, word])
			score = self.bigram_model.score([prev_word, word]) + self.unigram_model.score([word])

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

	def reverse_noun_adj(self, s):
		noun_tags = set(['NNP', 'NN', 'NNS'])
		adj_tags = set(['JJ'])
		parsed = parse.parse_english(s)[0]
		# print parsed
		words = parsed.words
		for i in range(len(words)-1):
			if parsed.tags[i] in noun_tags:
				if parsed.tags[i+1] in adj_tags:
					w = words[i]
					words[i] = words[i+1]
					words[i+1] = w
					print ">>>> SWITCHED %s and %s" % (w, words[i])
		words = ['^'] + words # stupid hack to make the formatting work
		# print words
		s = self.format(words)
		return s

	def remove_se(self, spanish_tokens):
		new_tokens = []
		for t in spanish_tokens:
			if t != "se":
				new_tokens.append(t)
			else:
				new_tokens.append("usted")
		return new_tokens



def main():
    """Tests the model on the command line. This won't be called in
        scoring, so if you change anything here it should only be code
        that you use in testing the behavior of the model."""

    print 'Building translator...'
    tranny = Translator('giddycorpus.txt')
    tranny.translate_sentence("Cuando se accede al ordenador como tal, pueden añadirse otros usuarios, configurar Usuarios Múltiples de Mac OS X, cambiar determinados ajustes del sistema y, en general, disponer de mayor acceso al sistema.")
    for i, (spanish_sentence, english_sentence) in enumerate(zip(ourdict.spanish_sentences, ourdict.english_sentences)):
     	#spanish_sentence = ourdict.spanish_sentences[i]
     	#english_sentence = ourdict.english_sentences[i]
    	translation = tranny.translate_sentence(spanish_sentence)
    	print "number: %d" % i
    	print "***ORIGINAL SENTENCE***: %s" % spanish_sentence
    	print "***OUR TRANSLATION***: %s" % translation
    	print "***ACTUAL TRANSLATION***: %s" % english_sentence
    	print "\n"


if __name__ == '__main__':
    main()
