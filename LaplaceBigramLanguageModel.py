import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    #
    self.word_unigramCounts = collections.defaultdict(lambda: 1)
    self.word_bigramCounts = collections.defaultdict(lambda: 1)
    
    self.pos_unigramCounts = collections.defaultdict(lambda: 1)
    self.pos_bigramCounts = collections.defaultdict(lambda: 1)

    #build ordered pos string, and ordered 
    #pos_orderings = 
    #sentences = 
    self.train(corpus)


  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    #builds bigram counts
    for sentence in corpus:
        # print sentence
        elems = sentence.split()
        # print elems
        bigram = "%s-%s" % (elems[1], elems[2])
        count = int(elems[0])
        self.word_bigramCounts[bigram] += count

    # Trains bigram model for 
    # for sentence in sentences:
    #     for i in xrange(0, len(sentence)):
    #         word = sentence[i]
    #         self.unigramCounts[word] = self.unigramCounts[word] + 1
    #         if (i >= 1):
    #             preword = sentence[i - 1]
    #             bigram = "%s-%s" % (preword, word)
    #             self.bigramCounts[bigram] = self.bigramCounts[bigram] + 1


    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.
    for i in xrange(0, len(sentence)):
        if (i >= 1):
            bigram = "%s-%s" % (sentence[i - 1], sentence[i])
            score += math.log(self.bigramCounts[bigram])
            preword = sentence[i - 1]
            score -= math.log(self.unigramCounts[preword] + len(self.bigramCounts))

    return score
