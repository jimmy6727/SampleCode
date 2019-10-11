# hmm_sequence.py
# Uses a hidden markov model as returned by hmm_model_build.py which is a list 
# in the form A_count, B_count, T_count
import math
import pickle

from nltk.util import ngrams
from nltk.corpus import brown
s = brown.tagged_sents(categories='news')
s = [sentence for sentence in brown.tagged_sents(categories='news')]
l = len(s)
#testset = s[:math.floor(0.1*l)]
testset = s

for i in range(len(testset)):
    sent = testset[i]
    sent.insert(0, ("<S>", "<S>"))
    testset[i] = sent
    
model = pickle.load(open('model.dat', 'rb'))
A = model[0]
B = model[1]
T = model[2]

logp = 0
for sent in testset[20:30]:
    prevtag = '<S>'
    for i in range(1,len(sent)-1):
        w = sent[i][0]
        t = sent[i][1]
        probTgivenTminusOne = A[prevtag][t] / sum(A[prevtag].values())
        prevtag = t
        logp += math.log(probTgivenTminusOne)
print(logp)
