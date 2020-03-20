from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import numpy as np
import nltk
from nltk.corpus import brown
#from nltk.corpus import stopwords
import random
import string
#import TextBlob as tb
import math
  
print("\n Paul: Hello, I am a chatbot named Paul. Please wait about 30 seconds while I teach myself the entirety of the english language.")

## Preprocess data and Build Corpus
corpus = brown.words(categories=['news', 'editorial', 'reviews', 
                                'religion', 'hobbies','lore',
                                'government', 'learned', 'fiction',
                                'mystery','adventure','romance'])

Mcorpus = ""
for w in corpus:
    Mcorpus += str(' '+str(w.lower()) + ' ')
        
# Convert to sentence tokens and word tokens
sent_tokens = nltk.sent_tokenize(Mcorpus)
word_tokens = nltk.word_tokenize(Mcorpus)
  
# Lemmatization functionality
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Hard coded greetings
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

# Greeting function
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

## Functionality to evaluate outputs
def build_model(train): 
    #list of lists(sentences) of tuples                            
    Acount = {} # 2D dictionary for tag to tag counts
    Bcount = {} # 2d dictionary for tag to word count
    for sentence in train:
        sentence = nltk.pos_tag(sentence)
        #print(sentence)
        prevtag = '<s>'
        for w,t in sentence:
            if t not in Bcount:
                Bcount[t] = {}
            if w not in Bcount[t]:
                 Bcount[t][w] = 1
            else:
                 Bcount[t][w] += 1
                    
            if prevtag not in Acount:   
                Acount[prevtag] = {}
            if t not in Acount[prevtag]:
                Acount[prevtag][t] = 1
            else:
                Acount[prevtag][t] += 1
            prevtag = t


    for tag1 in Acount.keys():
        count = 0
        for tag2 in Acount[tag1].keys():
            count += Acount[tag1][tag2]
        #print(count)
        for tag2 in Acount[tag1].keys():
            replace = Acount[tag1][tag2] / count
            Acount[tag1][tag2] = replace
            
    for tag1 in Bcount.keys():
        count = 0
        for tag2 in Bcount[tag1].keys():
            count += Bcount[tag1][tag2]
        #print(count)
        for tag2 in Bcount[tag1].keys():
            replace = Bcount[tag1][tag2] / count
            Bcount[tag1][tag2] = replace
    #print (Bcount)
    return Acount, Bcount

# Predict propbability of a given sentence
def sequence_prob(tagtagModel,wordtagModel, sentence):
    prevtag = '<s>'
    prob = 0 
    # print("Sentence in sequence_prob function: ", sentence)
    for word,tag in sentence:
        # print("point1___", prevtag, word, tag)
        # print("point1___", tagtagModel.keys())
        # print("point1___", tagtagModel[prevtag])
        if prevtag in tagtagModel.keys():
            if tag in tagtagModel[prevtag].keys():
                if tag == '<s>':
                    prob = 0.000000000001
                    prevtag = tag
                else:
                    prob = prob + tagtagModel[prevtag][tag]
                    prevtag = tag
        prevtag = tag
        if tag in wordtagModel.keys():
            if word in wordtagModel[tag].keys():
                # print("reaching point 4", word, tag)
                prob = prob + wordtagModel[tag][word]
        prevtag = tag
    # print("Prob: _____", prob)
    return prob


## Evaluate a sentence using a HMM tag model. Output the probability of a sentence
def Eval(sent,tagModel,wordModel):
    a = nltk.pos_tag(nltk.word_tokenize(sent))
    length = len(a)
    a.insert(0,('<s>', '<s>'))
    prob = sequence_prob(tagModel, wordModel, a)
    prob = (1/prob)**(1/length)
    return prob

## Response function to generate bot response given an input by the user.
def response(user_response,tagModel, wordModel):
    robo_response=''
    sent_tokens.append(user_response)
    tokenized = nltk.word_tokenize(user_response)
    
    # Uncomment the three lines below to run chatbot using non-noun stop words
    # from user response
    # isnt_noun = lambda pos: pos[:2] not in ['NN', 'NNP', 'NNS', 'VB', 'VBP', 'VBD']
    # nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if isnt_noun(pos)] 
    # sw = [word for (word, pos) in nltk.pos_tag(tokenized) if isnt_noun(pos)]
    
    # Uncomment the line below to run chatbot using all of user response as stop
    # words, including backoff
    sw = tokenized
    
    # run with stop_words = None, and with above line uncomented for other method
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words = sw)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    # Stopword Backoff used when we prohibit the bot from using any words that 
    # occured in the user input. We implemented this because the bot often just 
    # responded with a nearly identical statement to what we inputted.
    # Backoff was necessary because sometimes prohibiting all input words leads to 
    # TFIDF values of zero, meaning that the bot couldn't find anything to respond with.
    # In this case, we rerun the TFIDF calculation allowing the bot to use the last
    # word that we said, up to five levels of backoff.
    
    backoff_level = 0
    if(req_tfidf==0):
        for i in range(5):
            backoff_level += 1
            sw = user_response.split(' ')[:int(-1*backoff_level)]
            TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words = sw)
            tfidf = TfidfVec.fit_transform(sent_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx=vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]
            if req_tfidf != 0:
                robo_response = robo_response+sent_tokens[idx]
                print("""Perplexity of the tag sequence for bot response :""" + str(Eval(robo_response)))
                return robo_response
    if req_tfidf == 0:
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        
        # Uncomment the line below to see perplexity numbers
        #print('Perplexity of the tag sequence for bot response :'+str(Eval(robo_response,tagModel,wordModel)))

        return robo_response
    
    
def main():
    flag=True
    lists = []

    sentences = Mcorpus.split('.')
    for sentence in sentences:
        lists.append((nltk.word_tokenize(sentence)))
    tagModel, wordModel = build_model(lists)
    print("\n Paul: I am ready. Type something and press enter to talk to me. If you want to exit, type Bye!")
    while(flag==True):
        user_response = input()
        user_response=user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                print("Paul: You are welcome..")
            else:
                if(greeting(user_response)!=None):
                    print("Paul: "+greeting(user_response))
                else:
                    print(" ",end="")
                    r = response(user_response, tagModel, wordModel)
                    print("Paul: ",r, '\n')
                    sent_tokens.remove(user_response)
        else:
            flag=False
            print("Paul: Bye! take care..")
    
if __name__ == '__main__':
    main()
    
    