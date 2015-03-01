import subprocess						# for calling Stanford CoreNLP
import xml.etree.ElementTree as ET 		# to parse the XML output of CoreNLP

def main():
	# ________________________SPANISH ANNOTATION EXAMPLE___________________________________
	# Sample sentences that we need parsed and annotated
	spanish_sentences = ['Hola, como estas?', 'Me llamo Alejandro.', 'Ellos se llaman Eric, Pearson, y Gideon.', 'El gato gris solitario come mucho.']
	# Call the spanish parser/annotator and get back a list of parsed sentence objects
	parsed_spanish_sentences = parse_spanish(spanish_sentences)
	# Print some output
	for s in parsed_spanish_sentences:
		print s

	# ________________________ENGLISH ANNOTATION EXAMPLE___________________________________
	# Sample sentences that we need parsed and annotated
	english_sentences = ['Hi, how are you?', 'My name is Alejandro.', 'Their names are Eric, Pearson, and Gideon.', 'The lonely gray cat eats a lot.']
	# Call the english parser/annotator and get back an xml object root node
	parsed_english_sentences = parse_english(english_sentences)
	# Print some output
	for s in parsed_english_sentences:
		print s

#_________________________________________________________________________________________________

def parse(sentences, file_basename, command):
	# Put the sentences into a file in the parsing/spanish directory
	file_name = file_basename + '.txt'
	with open(file_name, 'w') as file_object:
		for sentence in sentences:
			file_object.write('%s\n' % sentence)
	subprocess.call(command, shell=True)
	# Put the output xml into a searchable python object
	xml_name = file_basename + '.xml'
	tree = ET.parse(xml_name)
	root = tree.getroot()
	parsed_sentences = []
	for sentence, sentence_node in zip(sentences, root.iter('sentence')):
		parsed_sentences.append(ParsedSentence(sentence, sentence_node))
	subprocess.call('rm %s' % (file_name), shell=True)
	subprocess.call('rm %s' % (xml_name), shell=True)
	return parsed_sentences

def parse_spanish(sentences, file_basename='PARSING_TMP'):
	file_name = file_basename + '.txt'
	command = 'java -cp "stanford-corenlp/*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -props StanfordCoreNLP-spanish.properties -file %s -replaceExtension >/dev/null 2>&1' % (file_name)
	return parse(sentences, file_basename, command)
	

def parse_english(sentences, file_basename='PARSING_TMP'):
	file_name = file_basename + '.txt'
	command = 'java -cp "stanford-corenlp/*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -props StanfordCoreNLP-english.properties -file %s -replaceExtension >/dev/null 2>&1' % (file_name)
	return parse(sentences, file_basename, command)

class ParsedSentence:
	def __init__(self, sentence, sentence_node):
		self.text = sentence
		self.words = [token.find('word').text for token in sentence_node.iter('token')]
		self.tags = [token.find('POS').text for token in sentence_node.iter('token')]
		self.parse_string = sentence_node.find('parse').text
	def __str__(self):
		return '\nSENTENCE: %s\nwords: %s\nPOS tags: %s\nparse string: %s\n' % (self.text, self.words, self.tags, self.parse_string)

if __name__ == '__main__':
	main()



