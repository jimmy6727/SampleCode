####################NOTES####################

#Probabilistic CFG's:
#    We now have probabilities associated with each of our production rules in the form
#    P(A -> B | A) where A -> B is a production and A is a constituent. We generally 
#    follow the rule:
#        Sum over all B of P(A -> B) always equals 1.
#        
#    Probability of parse tree T for sentence S:
#        P(T,S) = Product P(A -> B | A)
#        P(T,S) = P(T)P(S | T) = P(T) because we're not going to consider any trees that
#                                        don't match the sentence in question
#                    
#    T(S) = argmax(P(T)) We're just looking for the tree that maximizes the probability.

# Building a PCFG
#Counts: given a corpus of parsed sentences (called a treebank)
#    calculate the probability of a particular rule A -> B by counting number
#    of occurances of that rule divided by the sum of all rules with A on the 
#    left hand side.

#Evaluating output:
#    On a per constituent basis
#    A hypothesized constituent C_n is correct if there is a constituent 
#    in the reference C_r with the same wordwise starting point, wordwise ending 
#    point, and nonterminal symbol. We need all three to be correct.
#    Recall is the number of correct constituents in hypothesis divided by
#    number of constituents in reference. So if we have 8 correct terminals in 
#    our output and the correct reference tree has 10 terminals, our recall is 8/10.
#    Precision is the number of correct constituents in hypothesis divided by the total
#    number of constituents in hypothesis. So if our output tree has 8/11 terminals
#    correct, 8/11 is our precision.

#   F1-Measure: 2PR / P+R is the stat commonly reported.

#    In reality, the probability that an NP shows up depends on the other constituents
#    around it. The probability that an NP -> Pronoun is much higher at the beginning of 
#    a sentence and quite unlikely to show up at the end of english sentences, 
#    and an NP -> Det NN is much more likely at the end of a sentence, as an object.
#    NP -> pronoun has a 91% chance of being a subject and NP -> nonpronoun is only 9%
#    likely to be the subject. This is called positional context.
#    There is also lexical context - the idea that the words themselves influence the 
#    probability.


# Imports
import nltk
import re
from nltk.corpus import brown

# Accuracy Metric Calculation Functions
def Recall(reference, test):
    return sum(x == y for x, y in zip(reference, test)) / len(reference)

def Precision(reference, test):
    return sum(x == y for x, y in zip(reference, test)) / len(test)

def F1Score(reference, test):
    p = Precision(reference, test)
    r = Recall(reference, test)
    return((2*p*r)/(p+r))

# Build Vocab based on given corpus.
def build_vocab(corpus):
    v = {}
    
    for word in corpus:
        if word not in v:
            v[word] = 0
        if word in v:
            v[word] += 1
    
    v["<DollarSign>"] = 10
        
    print("Vocabulary of size "+str(len(v))+" built from given corpus.")
    return(v)
            
# Replace all words within given set of trees that aren't in a given
# vocabulary with <UNK> token.    
def replace_unknown_words(trees, vocab):
    new_trees = []
    for t in trees:
        t_string = ' '.join(str(t).split()) 
        # Make sure there are no special characters (asterisks, etc.)
        # that could mess up the regex search
        for c in ['*', '0','-1','-2', '...']: 
            t_string=t_string.replace(c,"")
        t_string = t_string.replace("$", "<DollarSign>")
        st = nltk.tree.Tree.fromstring(t_string)
        wt = st.leaves()
        for word in wt:
            if word not in vocab: 
                t_string = re.sub(str(word), "<UNK>", t_string)
        t_string = re.sub("<<UNK>NK>", "<UNK>", t_string)
        t = nltk.tree.Tree.fromstring(t_string)
        new_trees.append(t)
        
    return(new_trees)

# Train
def pcfg_train(trees, vocab):
#    Write a function pcfg_train() that takes as its input a collection 
#    of nltk.tree.Tree objects. For example, it might be passed some 
#    portion of nltk.corpus.treebank.parsed_sents(). This function 
#    should return a nltk.PCFG object.
    
    all_productions = []
    
    for t in trees:
        for p in t.productions():
            all_productions.append(nltk.Production(p.lhs(), p.rhs()))
            
    pcfg = nltk.induce_pcfg(nltk.Nonterminal('S'), all_productions)
       
    return(pcfg)

# Test  
def pcfg_test(pcfg, trees, correct_trees, vocab):
#    Write a function pcfg_test() that takes as its input a nltk.PCFG object, 
#    and a collection of nltk.tree.Tree objects. Within this function, use an 
#    nltk.ViterbiParser built from your PCFG to parse the sentences from the 
#    trees you have been given. Then, compare your highest-probability parses 
#    with the correct parses that your function has been given. Measure recall 
#    and precision for each sentence in your test set, and report overall 
#    recall, precision and F1 score for all sentence in your test set. Have 
#    this function print out your results.
    
    
    s = str(pcfg.productions())
    missing = []
    edited_trees = []
    for t in trees:
        t_string = str(t)
        for word in t.leaves():
            if word not in s:
                print(word)
                missing.append(word)
                t_string = re.sub(word, "<UNK>", t_string)
        new = nltk.Tree.fromstring(t_string)
        edited_trees.append(new)
        
    print(str(len(missing)) + " words from testset missing from grammar vocabulary during testing. \n")
    
    # Instantiate parser
    vp = nltk.ViterbiParser(pcfg)
       
    ## Accuracy stats

#    A hypothesized constituent C_n is correct if there is a constituent 
#    in the reference C_r with the same wordwise starting point, wordwise ending 
#    point, and nonterminal symbol. We need all three to be correct.
#    Recall is the number of correct constituents in hypothesis divided by
#    number of constituents in reference. So if we have 8 correct terminals in 
#    our output and the correct reference tree has 10 terminals, our recall is 8/10.
#    Precision is the number of correct constituents in hypothesis divided by the total
#    number of constituents in hypothesis. So if our output tree has 8/11 terminals
#    correct, 8/11 is our precision.

#   F1-Measure: 2PR / P+R is the stat commonly reported.
    
## Build a list of the ranges of constituents in reference. A 1-4, C 2-4, E 2-2
# Replace bottom node (the one that is just A->"word") with a tree structure A->1
# Test if each range of constituents is in the reference list
    
    for i in range(len(edited_trees)):
        t = edited_trees[i]
        correct_terminals = correct_trees[i].leaves()
        print("Analyzing sentence: "+str(correct_terminals)+"\n")
        sent = t.leaves()
        print("Finding most probable parse for tokens: "+ str(sent)+"\n")
        parses = vp.parse(sent)
        for p in parses:
            print("Predicted most likely parse tree: \n")
            print(p)
            print(p.leaves())
            print("Recall :" +str(Recall(correct_terminals, p.leaves())))
            print("Precision :" + str(Precision(correct_terminals, p.leaves())))
            print("F1 Score :"+str(F1Score(correct_terminals, p.leaves())))
            print("\n\n")

def main():
    # Build vocabulary dictionary from brown corpus 
    Mvocab = build_vocab(corpus = brown.words(categories=['news', 'editorial', 'reviews', 
                                                         'religion', 'hobbies','lore',
                                                         'government', 'learned', 'fiction',
                                                         'mystery','adventure','romance']))
    
    # Separate out training trees 
    train_trees = nltk.corpus.treebank.parsed_sents()[:1000]
    
    # Replace unknown words
    train_trees = replace_unknown_words(train_trees, Mvocab)
    
    # Test on test trees and display results
    Mpcfg = pcfg_train(train_trees, Mvocab)
    correct_test_trees = nltk.corpus.treebank.parsed_sents()[1002:1005]
    test_trees = replace_unknown_words(correct_test_trees, Mvocab)
    pcfg_test(Mpcfg, test_trees, correct_test_trees, Mvocab)

main()

#################### Output ####################
#
#Vocabulary of size 49978 built from given corpus.
#No.
#alone
#competitors
#3 words from testset missing from grammar vocabulary during testing. 
#
#Analyzing sentence: ['The', 'company', 'also', 'disclosed', 'that', 'during', 'that', 'period', 'it', 'offered', '10,000', 'yen', ',', 'or', 'about', '$', '70', '*U*', ',', 'for', 'another', 'contract', '.']
#
#Finding most probable parse for tokens: ['The', 'company', 'also', 'disclosed', 'that', 'during', 'that', 'period', 'it', 'offered', '<UNK>', 'yen', ',', 'or', 'about', '<DollarSign>', '7', 'U', ',', 'for', 'another', 'contract', '.']
#
#Predicted most likely parse tree: 
#
#(S
#  (NP-SBJ (DT The) (NN company))
#  (ADVP-TMP (RB also))
#  (VP
#    (VBD disclosed)
#    (SBAR
#      (WHNP (WDT that))
#      (S
#        (PP-LOC (IN during) (NP (DT that) (NN period)))
#        (NP-SBJ (PRP it))
#        (VP
#          (VBD offered)
#          (ADJP-PRD
#            (ADJP
#              (ADJP (CD <UNK>) (NN yen))
#              (, ,)
#              (CC or)
#              (ADJP
#                (QP
#                  (IN about)
#                  (<DollarSign> <DollarSign>)
#                  (CD 7))
#                (-NONE- U))
#              (, ,))
#            (PP (IN for) (NP (DT another) (NN contract)))))
#        (. .))))) (p=2.36035e-57)
#['The', 'company', 'also', 'disclosed', 'that', 'during', 'that', 'period', 'it', 'offered', '<UNK>', 'yen', ',', 'or', 'about', '<DollarSign>', '7', 'U', ',', 'for', 'another', 'contract', '.']
#Recall :0.8260869565217391
#Precision :0.8260869565217391
#F1 Score :0.8260869565217391
#
#
#
#Analyzing sentence: ['But', 'Fujitsu', ',', 'Japan', "'s", 'No.', '1', 'computer', 'maker', ',', 'is', "n't", 'alone', '.']
#
#Finding most probable parse for tokens: ['But', '<UNK>', ',', 'Japan', '<UNK>', '<UNK>', '1', 'computer', 'maker', ',', 'is', '<UNK>', '<UNK>', '.']
#
#Predicted most likely parse tree: 
#
#(S
#  (CC But)
#  (NP-SBJ (-NONE- <UNK>))
#  (PRN
#    (, ,)
#    (NP-SBJ (NNP Japan) (NNP <UNK>))
#    (VP
#      (VBG <UNK>)
#      (NP-EXT (CD 1) (NN computer))
#      (NP-TMP (NN maker)))
#    (, ,))
#  (VP (VBZ is) (NP (NNP <UNK>) (NNP <UNK>)))
#  (. .)) (p=6.8798e-29)
#['But', '<UNK>', ',', 'Japan', '<UNK>', '<UNK>', '1', 'computer', 'maker', ',', 'is', '<UNK>', '<UNK>', '.']
#Recall :0.6428571428571429
#Precision :0.6428571428571429
#F1 Score :0.6428571428571429
#
#
#
#Analyzing sentence: ['NEC', ',', 'one', 'of', 'its', 'largest', 'domestic', 'competitors', ',', 'said', '0', 'it', 'bid', 'one', 'yen', 'in', 'two', 'separate', 'public', 'auctions', 'since', '1987', '.']
#
#Finding most probable parse for tokens: ['<UNK>', ',', 'one', 'of', 'its', 'largest', 'domestic', '<UNK>', ',', 'said', 'it', 'bid', 'one', 'yen', 'in', 'two', 'separate', 'public', '<UNK>', 'since', '<UNK>', '.']
#
#Predicted most likely parse tree: 
#
#(S
#  (NP-SBJ
#    (NP (-NONE- <UNK>))
#    (, ,)
#    (NP
#      (NP (CD one))
#      (PP
#        (IN of)
#        (NP
#          (PRP<DollarSign> its)
#          (NX (JJS largest) (JJ domestic) (NN <UNK>)))))
#    (, ,))
#  (VP
#    (VBD said)
#    (S
#      (NP-SBJ (PRP it))
#      (VP
#        (VBD bid)
#        (NP-EXT (CD one) (NN yen))
#        (PP-DIR
#          (IN in)
#          (NP
#            (NP (CD two))
#            (JJ separate)
#            (JJ public)
#            (NN <UNK>)))
#        (PP-LOC (IN since) (NP (-NONE- <UNK>))))
#      (. .)))) (p=1.45154e-54)
#['<UNK>', ',', 'one', 'of', 'its', 'largest', 'domestic', '<UNK>', ',', 'said', 'it', 'bid', 'one', 'yen', 'in', 'two', 'separate', 'public', '<UNK>', 'since', '<UNK>', '.']
#Recall :0.34782608695652173
#Precision :0.36363636363636365
#F1 Score :0.3555555555555555
#
#
#
