# POSTagging.py

# P(ti | ti-1) probability of a tag bigram - the transition probability
# P(wi | ti) probability of a word given a tag - the emission probability

# Given the sentence "I want to race" we can calculate the highest probability
# tag sequence. The sentence could be tagged as "I/PRP want/VB to/TO race/VB"
# or as "I/PRP want/VB to/TO race/NN"
#
# The calculation goes as follows: 
# First tag sequence = P("I"|PRP)*P(VB|PRP)*P("want"|VB)*P(TO|VB)*P("to"|TO)*P(VB|TO)*P("race"|VB)
# Second tag sequence = P("I"|PRP)*P(VB|PRP)*P("want"|VB)*P(TO|VB)*P("to"|TO)*P(NN|TO)*P("race"|NN)
# And obviously the highest probability is more likely. 
# With log probs, we add.
                                

# This gives us the more likely tag sequence between the two. But now what if we're interested
# in the MOST LIKELY tag sequence out of all possible sequences - which in reality we are - we denote this
# as ARGMAX(P(ti^n | wi^n)) = Product from i = 1 to n of P(wi | ti)*P(ti | ti-1)

# Technically, this requires us to calculate 45^n possibilities, but we can estimate it - in class notes

#from nltk.util import ngrams
#from nltk.corpus import brown
#s = brown.tagged_sents(categories='news')

#file = "/Users/jimmyjacobson/Downloads/greeneggs_tagged.dat"
#f = open(file, 'rb')
#f1 = pickle.load(f)
    
#def AddSentenceBoundaries(datafile):
#    for s in datafile:
#        print(s)
#        print(s[0])
#        print(s[0][1])
#        s_len = len(s)
#        print(s_len)
#        #Beginning of sentence tag bigram
#        s.append(("<s>", s[0][1]))
#        print(s)
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
               
        #return(self.A_count, self.B_count, self.T_count)
        
def main():
    s = brown.tagged_sents(categories='news')
    print("Building Hidden Markov Model for brown news corpus")
    #file = sys.argv[1]
    #print("Building Hidden Markov Model for file " + str(file))
    #f = pickle.load(open(file, 'rb'))
    Model = HMTagModel(s)
    Model.WriteModelToFile('model.dat')

if __name__ == '__main__':
    main()
#
#PofNNgivenDT = A_count['DT']['NN'] / T_count['DT']
#print(A_count)
#print("\n\n\n")
#print(B_count)
#print("\n\n")
#print(PofNNgivenDT)
