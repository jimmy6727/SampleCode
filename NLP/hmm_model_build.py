## Hidden Markov Model Part of Speech Tagger 
## This model-building script takes a command line argument of a binary, pre-tagged training corpus and builds probability
## matrices for use in predictive part of speech analysis of text.

# P(ti | ti-1) probability of a tag bigram - the transition probability
# P(wi | ti) probability of a word given a tag - the emission probability

import sys
import pickle
from nltk.corpus import brown

class HMTagModel:
    
    def __init__(self, word_tag_corpus):
        self.BuildDictionaries(word_tag_corpus)
    
    def WriteModelToFile(self, filename):
        print("Saving to " + str(filename))
        pickle.dump([self.A_count, self.B_count, self.T_count], open(filename, "wb" ) )
        
    def BuildDictionaries(self, word_tag_corpus):
        tags = []
        words = []
        self.A_count = {}
        self.B_count = {}
        self.T_count = {}
        
        for sent in word_tag_corpus:
            prevtag = '<S>'
            for w,t in sent:
               tags.append(t)
               words.append(w)
               
               # Tag unigram counts
               if t not in self.T_count:
                   self.T_count[t] = 1
               else:
                   self.T_count[t] += 1
                    
                # B count - Counts of word given tag
               if t not in self.B_count:
                   self.B_count[t] = {} 
               if w not in self.B_count[t]:
                   self.B_count[t][w] = 1
               else:
                   self.B_count[t][w] += 1
              
                # A count - tag bigram counts
               if prevtag not in self.A_count:
                   self.A_count[prevtag] = {}
               if t not in self.A_count[prevtag]:
                   self.A_count[prevtag][t] = 1  
               else:
                   self.A_count[prevtag][t] += 1
            
               prevtag = t
               
        
def main():
    s = brown.tagged_sents(categories='news')
    print("Building Hidden Markov Model for brown news corpus")
    Model = HMTagModel(s)
    Model.WriteModelToFile('model.dat')

if __name__ == '__main__':
    main()

