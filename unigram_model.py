import math, collections

class LaplaceUnigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramLapCounts = collections.defaultdict(lambda: 1)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    
    first = True
    for line in corpus:
      line = line.split()
      for word in line: 
        if self.unigramLapCounts[word] < 2:
          self.total += 1 
        self.unigramLapCounts[word] += 1

###
    #   middle = line.split()[1]
    #   num = line.split()[0]
    #   if (first):
    #     uni_word = middle
    #     self.total += 1
    #     first = False
    #   elif middle != uni_word:
    #     uni_word = middle
    #     self.total += 1
    #   self.unigramLapCounts[uni_word] += int(num)
    # self.total += len(self.unigramLapCounts)
    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    for token in sentence:
      count = self.unigramLapCounts[token]
      score += math.log(count)
      score -= math.log(self.total)
    return score