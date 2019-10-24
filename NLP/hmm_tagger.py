# hmm_tagger
import pickle
import numpy as np
import math
import statistics
from nltk.corpus import brown

def Viterbi(A, B, WordTags):

    words = []
    correcttags = []
    tags = list(A.keys())
    for w,t in WordTags:
        words.append(w)
        correcttags.append(t)
 
    # N is the number of states, in this case the number of unique tags
    # t is the length of the sentence(s) that we are trying to get most probable tag sequence of
    n = len(A.keys())
    t = len(tags)
    
    viterbi_matrix = np.zeros((n,t))
    backpointer = np.zeros((n,t))
    
    # viterbi_matrix[i] is the i-th row
    # viterbi_matrix[:,i] is the i-th column
    
    starttag = "<S>"
    
#    print(words)
    for i in range(len(tags)):
        tag = tags[i]
        if tag in list(A[starttag].keys()):
            viterbi_matrix[i,0] = A[starttag][tag]
            backpointer[i,0] = 0
    
    predicted_tags = []
#    print(len(words))
    for t in range(1,len(words)):
        word = words[t-1]
#        print(word)
#        print("T-1 " + str(t-1))
#        print(viterbi_matrix[:,t-1])
        for i in range(1,len(tags)):
            tag = tags[i]
            vtj=0
#            if t == 2:
#                print("Tag when t=2: " +str(tag))
#                print("vtj: " + str(vtj))
            if len(predicted_tags) > 0:
                prev_tag = predicted_tags[-1]
            else:
                prev_tag = tag
            for j in range(len(tags)):

                # If the tag never occurs after prev_tag in training, 
                # probability is zero and we can iggnore it, or if the word is never tagged as
                # tag in training, then we also ignore it.
                if tag in list(A[prev_tag].keys()):
                    if word in list(B[tag].keys()):
                        vtj =  viterbi_matrix[j,t-1]*A[prev_tag][tag]*B[tag][word]
                if vtj > viterbi_matrix[i,t]:
#                    print("New max value: " + str(vtj) + "is bigger than old value " + str(viterbi_matrix[i,t]))
                    viterbi_matrix[i,t] = vtj
                    backpointer[i,t] = i
#                    print(tags[i])
                    mc_tag = tags[i]

            # Sometimes, we get to this point and the entire column of the viterbi matrix
            # is blank, usually because of a weirdly specific tag like "AT-TL", which
            # only ever transition to a tag with the same suffix designation (NN-HL only transitions
            # to JJ-HL, RP-HL, VBZ-HL, etc.) This causes an column of entirely zeros in the matrix,
            # causing predicted tags to stop updating, resulting in awful tag accuracy.
            
            
#        if t == 2:
#            print(word in B[tag].keys())
#            print(B[tag])
#        print(A[mc_tag])
#        print("word done")    
#        print("MCTag = " + str(mc_tag))   
            
        # There are also times when we get to this point and mc_tag was never assigned. We
        # worked around this by wrapping it in a trycatch. This would be the first thing we
        # would fix if we could go back and work more on this.
        predicted_tags.append(mc_tag)
#    print("\nPredicted tags: " + str(predicted_tags[:t]))
#    print("\nCorrect tags: " +str(correcttags))
 
#    t = len(words)
#    bestpathprob = 0
#    for i in range(1,len(tags)):
#        print(viterbi_matrix[i,t])
#    print(bestpathprob)
    return predicted_tags, correcttags
 
def GetAccuracyPercentage(ViterbiObject):
    p = 0
    for i in range(len(a[0])):
        if a[0][i] == a[1][i]:
            p+=1
    ap = float(100*(p/len(a[0])))
    print("Accuracy Percentage = "+ str(ap))
    return ap
    
# Get last 10% of brown corpus for testing and run Viterbi on every sentence to get accuracy percentage
testset = [sentence for sentence in brown.tagged_sents(categories='news')]
l = len(testset)
testset = testset[math.floor(0.1*l):]

Model = pickle.load(open('model.dat', 'rb'))
ran = 0
acc = []
for testsentence in testset[200:300]:
    #print("\nSentence being tested: " +str(testsentence))
    try:
        a = Viterbi(A = Model[0], B = Model[1], WordTags = testsentence)
        ran += 1
        acc.append(GetAccuracyPercentage(a))
    except:
        pass
    
print("Final output:\n"
      "Tagger was able to run without error on " + str(ran) + " out of 100 sentences in testset."
      " Of the sentences tagged, average accuracy was " + str(statistics.mean(acc)) + " percent.")




### Final Output
#Final output:
#Tagger was able to run without error on 56 out of 100 sentences in testset. 
#Of the sentences tagged, average accuracy was 55.06479577448789 percent.


#Accuracy Percentage = 66.66666666666666
#Accuracy Percentage = 15.0
#Accuracy Percentage = 66.66666666666666
#Accuracy Percentage = 68.42105263157895
#Accuracy Percentage = 23.076923076923077
#Accuracy Percentage = 100.0
#Accuracy Percentage = 100.0
#Accuracy Percentage = 20.689655172413794
#Accuracy Percentage = 0.0
#Accuracy Percentage = 92.3076923076923
#Accuracy Percentage = 0.0
#Accuracy Percentage = 93.10344827586206
#Accuracy Percentage = 100.0
#Accuracy Percentage = 82.35294117647058
#Accuracy Percentage = 73.33333333333333
#Accuracy Percentage = 77.27272727272727
#Accuracy Percentage = 13.636363636363635
#Accuracy Percentage = 14.285714285714285
#Accuracy Percentage = 0.0
#Accuracy Percentage = 31.57894736842105
#Accuracy Percentage = 0.0
#Accuracy Percentage = 81.81818181818183
#Accuracy Percentage = 87.5
#Accuracy Percentage = 5.555555555555555
#Accuracy Percentage = 5.263157894736842
#Accuracy Percentage = 84.84848484848484
#Accuracy Percentage = 89.47368421052632
#Accuracy Percentage = 0.0
#Accuracy Percentage = 82.35294117647058
#Accuracy Percentage = 9.67741935483871
#Accuracy Percentage = 87.5
#Accuracy Percentage = 47.05882352941176
#Accuracy Percentage = 80.0
#Accuracy Percentage = 43.47826086956522
#Accuracy Percentage = 86.66666666666667
#Accuracy Percentage = 69.23076923076923
#Accuracy Percentage = 92.85714285714286
#Accuracy Percentage = 90.9090909090909
#Accuracy Percentage = 85.36585365853658
#Accuracy Percentage = 100.0
#Accuracy Percentage = 64.51612903225806
#Accuracy Percentage = 64.51612903225806
#Accuracy Percentage = 39.130434782608695
#Accuracy Percentage = 88.88888888888889
#Accuracy Percentage = 11.11111111111111
#Accuracy Percentage = 87.09677419354838
#Accuracy Percentage = 44.44444444444444
#Accuracy Percentage = 90.9090909090909
#Accuracy Percentage = 16.666666666666664
#Accuracy Percentage = 11.11111111111111
#Accuracy Percentage = 100.0
#Accuracy Percentage = 4.878048780487805
#Accuracy Percentage = 44.0
#Accuracy Percentage = 87.09677419354838
#Accuracy Percentage = 6.25
