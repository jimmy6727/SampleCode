## N Gram Language Model
## This language model program takes two command line arguments - first the modelfile corpus to use for building the bigram
## language model, and second the testfile that we are interested in predicting the author of.

import re
import sys
import nltk
import numpy as np
from nltk.util import ngrams
import math

modelfile = sys.argv[1]
testfile = sys.argv[2]

def ParseTestAndTrainingModelsFile(file):

    f = open(file, 'r')
    authors_files_list = []
    for lines in f:
        line = re.split('\s', lines)
        authors_files_list.append(line)

    return(authors_files_list)
    
def TokenizeFile(filename):
    f = open(filename, 'r')
    tokens = []
    for line in f:
        tokens += NoPuncTokenizeString(string = str(line))
    f.close()
    return tokens 

def HandleTestFile(t):

    for i in range(len(t)):
        a = t[i][0]
        files = t[i][1:]
    return(t)
    
def NoPuncTokenizeString(string):
    
    string = re.sub(r'([\-:;"@,#$%^.,!?&*\(\)])', '', string)
    c = re.split("\s+", string)
    return c

class LanguageModel:
    
    def __init__(self, modelfilelist):
    # Class constructor #
    
        # Removes empty strings from modelfilelist
        modelfilelist = [i for i in modelfilelist if i]                         
        
        # Clean up commas
        a = modelfilelist[0]                                                    
        a = re.sub(r',','',a)
        
        # Set author and create empty list to populate for vocabulary
        self.author = a
        self.vocabulary = []
        
        # Build vocabulary
        for f in modelfilelist[1:]:
            # Clean up commas again
            f = re.sub(r',','',f)
            self.vocabulary += self.TokenizeFile(f)
        
        # Removes empty strings from vocabulary
        self.vocabulary = [i for i in self.vocabulary if i]                     
        
        # Count unigram frequencies
        self.unigramCounts = {}
        for word in self.vocabulary:
            if word in self.unigramCounts:
                self.unigramCounts[word] += 1
            else:
                self.unigramCounts.update({word: 1})
         
        # Get word length of training corpus and use to get devset
        self.training_word_length = len(self.vocabulary)
        self.devset = self.vocabulary[50:(math.ceil(0.1*self.training_word_length))]
        
        # |V| = vocab size
        self.size_vocabulary = len(np.unique(self.vocabulary))
        
        # Build N-Gram Collections
        self.bigrams = self.GetNGrams(self.vocabulary, n=2)
        self.trigrams = self.GetNGrams(self.vocabulary, n=3)

        # N_c values - the number of unique n-grams that appear c times. For 1<C<10
        # and the sum of all of them for use in GT Smoothing
        self.totalnr = 0
        for i in range(11):
            s = sum(x == i for x in self.unigramCounts.values())
            ni = str("n"+str(i))
            self.totalnr += s
            setattr(self, ni, s)
    
    def PrintLanguageModel(self):
        print("\nPrinting Language Model for " + str(self.author))
        print("\nLanguage Model built on text of length " + str(self.training_word_length) + " words")
        print("\nNumber of unique unigrams = |V| = " + str(self.size_vocabulary))
        print("\nVocabulary Sample: "+ str(self.vocabulary[:20]))
        print("\nSample bigrams: " + str(self.bigrams[:20]))
        print("\nSample trigrams: " + str(self.trigrams[:20]))
        print("\nSample of devset: " + str(self.devset[:20]))
        print("\nSample of unigram counts: " + str( {k: self.unigramCounts[k] for k in list(self.unigramCounts)[:20]}))
        print("\nNc values: ")
        print("N1 = " + str(self.n1))
        print("N2 = " + str(self.n2))
        print("N3 = " + str(self.n3))
        print("N4 = " + str(self.n4))
        print("N5 = " + str(self.n5))
        print("N6 = " + str(self.n6))
        print("N7 = " + str(self.n7))
        print("N8 = " + str(self.n8))
        print("N9 = " + str(self.n9))
        print("N10 = " + str(self.n10))
        print("Sum nR = " + str(self.totalnr))
        
        
    def NoPuncTokenizeString(self, string):
        
        string = re.sub(r'([\-:;"@,#$%^.,!?&*\(\)])', '', string)
        c = re.split("\s+", string)
        return c
    
    def GetNGrams(self, tokenlist, n):
        grams = list(ngrams(tokenlist, n))
        return grams
    
    def TokenizeFile(self, filename):
        f = open(filename, 'r')
        tokens = []
        for line in f:
            tokens += self.NoPuncTokenizeString(string = str(line))
        f.close()
        return tokens 
        
    def GetMatches(self, to_match, gramlist):
        count = 0
        matches = []
        for g in gramlist:
            if g[0] == to_match:
                matches.append(g)
                count = count +1
                
        if (len(matches)) == 0:
            return(0)
        else:
            return(matches)
            
    def GetProbability(self, to_match, given, gramlist):
        #Get length of grams that we're working with
        n = len(gramlist[0])
        
        #Get matches for the given words
        matches = self.GetMatches(given, gramlist)
        
        if matches == 0:
            #print("No Matches in Get Probability Function")
            return self.HandleUnknownWord(to_match, given, gramlist)
        
        else:
            #Counts to use for probability calculations
            given_c = len(matches)
            match_c = 0
            
            for i in range(len(matches)):
                if matches[i][n-1] == to_match:
                    match_c = match_c+1
                    
            return((match_c)/(given_c))
            
    def cStar(self, c):
        # Good-Turing Star Function
        
        s = "n"+str(c)
        nc = getattr(self, s)
        
        s1 = "n"+str(c+1)
        nc1 = getattr(self, s1)
    
        a = (c+1)*(nc1/nc)

        return(a)
        
    def HandleUnknownWord(self, to_match, given, gramlist):
        # Zeroes in the matrix can be smoothed with Good Turing Smoothing: C* = (c+1)(N_{c+1} / N_c) where N_c is the number of unique
        # n-grams that appear exactly c times in the training corpus. So if there are 10000 unique bigrams that appear twice, and 5000 
        # unique bigrams that appear three times the equation would look like (2+1)(10000/5000) = 6
        rstar = self.cStar(1)
        a = (rstar / self.totalnr)
        
        return a
    
    def GetProbabilityOfSequence(self, word_sequence, gramlist):
        # P(w1w2 ... wn) = P(w1)P(w2|w1)P(W3|W2) ... P(Wn|Wn-1)
        
        probabilities = []
        for i in range(len(word_sequence)-1):
            p = self.GetProbability(word_sequence[i+1], given = word_sequence[i], gramlist = gramlist)
            #print(p)
            if p != 0:
                probabilities.append(p)
        
        a = sum(math.log(p) for p in probabilities)
        print("Log probability of author " + str(self.author) +" = " + str(sum(math.log(p) for p in probabilities)))
        return(a)
    
def main():
    models = ParseTestAndTrainingModelsFile(modelfile)
    AustenModel = LanguageModel(modelfilelist = models[0])
    DickensModel = LanguageModel(modelfilelist = models[1])
    
    t = ParseTestAndTrainingModelsFile(testfile)
    t = HandleTestFile(t)
    
    for i in range(len(t)):
        correct_author = t[i][0]
        c_a = re.sub(r',','',str(correct_author))
        print("Correct Author = " +c_a + "\n")
        for j in range(1,len(t[i])-1):
            f = str(t[i][j])
            f = re.sub(r',','',str(f))
            print("testing file " + str(f))
            fl = TokenizeFile(f)
            a = AustenModel.GetProbabilityOfSequence(fl, AustenModel.bigrams)
            d = DickensModel.GetProbabilityOfSequence(fl, DickensModel.bigrams)
            if a < d:
                print("Models predict author = Austen \n\n")
            elif d < a:
                print("Models predict author = Dickens \n\n")
                
    return

main()

## Outout and results:

#My models predicted three of the six test files accurately. It was notable to me that 
#they actually got 5 of the 6 test files correct when I left zero probabilities unsmoothed and
#didn't include them in the count. However I opted for the more theoretically correct 
#implementation. 
#
#Outout: 
#    Jimmys-MacBook-Pro-4:PythonScripts jimmyjacobson$ python3 LanguageModel.py modelfile1.txt testfile1.txt
#Correct Author = austen
#
#testing file austen1.txt
#Log probability of author austen = -235.9424479897352
#Log probability of author dickens = -226.03761648926843
#Models predict author = Austen 
#
#
#testing file austen2.txt
#Log probability of author austen = -377.18160706898277
#Log probability of author dickens = -402.33585822355036
#Models predict author = Dickens 
#
#
#testing file austen3.txt
#Log probability of author austen = -210.4882923433502
#Log probability of author dickens = -207.48067804210731
#Models predict author = Austen 
#
#
#Correct Author = dickens
#
#testing file dickens1.txt
#Log probability of author austen = -172.27871628137083
#Log probability of author dickens = -161.61692015306264
#Models predict author = Austen 
#
#
#testing file dickens2.txt
#Log probability of author austen = -293.1390865567403
#Log probability of author dickens = -269.81128346725274
#Models predict author = Austen 
#
#
#testing file dickens3.txt
#Log probability of author austen = -238.30380988387282
#Log probability of author dickens = -248.0395111133914
#Models predict author = Dickens 


