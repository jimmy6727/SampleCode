# hmm_sequence.py
# Uses a hidden markov model as returned by hmm_model_build.py which is a list 
# in the form A_count, B_count, T_count
import math
import pickle
from nltk.corpus import brown

# Convert type to mutable type 
s = [sentence for sentence in brown.tagged_sents(categories='news')]
l = len(s)
testset = s[:math.floor(0.05*l)]

for i in range(len(testset)):
    sent = testset[i]
    sent.insert(0, ("<S>", "<S>"))
    testset[i] = sent
    
model = pickle.load(open('model.dat', 'rb'))
A = model[0]
B = model[1]
T = model[2]

# P(wi | ti)*P(ti | ti-1)

logp = 0
for sent in testset[25:26]:
    #print(sent)
    prevtag = '<S>'
#    for i in range(1,len(sent)-1):
#        w = sent[i][0]
#        print(w)
#        t = sent[i][1]
#        print(t)
    for w,t in sent:

        if t in list(A[prevtag].keys()):
            probTgivenTminusOne = A[prevtag][t]
            print(probTgivenTminusOne)
            
        elif t not in list(A[prevtag].keys()):
            print("Tag not found " + str(t))
            probTgivenTminusOne = 0
            
        if w in list(B[prevtag].keys()):
            probWgivenT = B[prevtag][w]
            print(probWgivenT)
            
        # Handle unknown words based on common suffixes
        elif w not in list(B[prevtag].keys()):
            print("Word not found " + str(w))
            # If word ends in -ed, it is likely to be a VBD.
            if w[-2:] == 'ed':      # painted
                print("Suffix match found for " +str(w))
                probWgivenT = max(B['VBD'].values())
            # Verb
            elif (w[-3:] == 'ate' or  # germinate
                w[-3:] == 'ify' or  # clarify
                w[-3:] == 'ize'):   # harmonize
                print("Suffix match found for " +str(w))
                probWgivenT = max(B['VB'].values())
            # Noun
            elif (w[-3:] == 'ist' or  # florist, dentist
                w[-2:] == 'er' or   # painter, designer
                w[-3:] == 'ion' or  # action, reaction
                w[-4:] == 'ment' or # encouragement, resentment
                w[-4:] == 'ence' or # confidence
                w[-4:] == 'ness' or # willingness
                w[-4:] == 'ship' or # friendship
                w[-3:] == 'ity'):   # charity, clarity
                print("Suffix match found for " +str(w))
                probWgivenT = max(B['NN'].values())
            # Plural noun
            elif w[-1:] == 's':
                print("Suffix match found for " +str(w))
                probWgivenT = max(B['NNS'].values())
            # We have a lot of common adjective suffixes
            elif (w[-4:] == 'able' or # adjustable
                w[-3:] == 'ful' or  # wonderful
                w[-4:] == 'less' or # mindless
                w[-3:] == 'ous' or  # joyous
                w[-2:] == 'al' or   # emotional
                w[-3:] == 'ish' or  # childish
                w[-2:] == 'ic' or   # athletic
                w[-3:] == 'ive'):   # subjective
                print("Suffix match found for " +str(w))
                probWgivenT = max(B['JJ'].values())
            
            else:
                print("No suffix match found")
                
        if logp <= 0:
            logp += math.log(probTgivenTminusOne*probWgivenT)
        
        prevtag = t

print("Probability of given tag sequence for sentence: " + str(logp))