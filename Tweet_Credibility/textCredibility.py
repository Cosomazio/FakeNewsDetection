import os
import re
import numpy as np
import string
from xgboost import XGBClassifier
from spellchecker import SpellChecker
from spamdetectorNLP import predictText
from SPAMDetectorFeatureExtractor import *
from feature_extraction.twitter_api import *


def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    return testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()
    
def getText(tweet_id):
    v1_connection = api_v1_connection()
    #v2_connection = api_v2_connection()
    status = get_tweet_status(tweet_id, v1_connection)
    # data = json.load(file)
    # text = data['text']
    # file.close()

    return status.text

def isSpamXGB(testo):
    feature=features_extraction(testo)
    x = np.array(feature, dtype="int").reshape((1,len(feature)))
    #print(x.shape)
    model = XGBClassifier()
    model.load_model("./Tweet_Credibility/spamdetector.json")
    pred = model.predict(x)
    return True if pred == 0 else False

def isSpamNLP(testo):
    return 0 if predictText(testo) else 100


def badWords(testo):
    with open(os.path.realpath(os.path.dirname(__file__))+'/bad_words.txt', 'r') as badDict:
        profanities = badDict.readlines()

    testo=cleanText(testo)
    testo=testo.split()

    checker = SpellChecker()
    mispelled = checker.unknown(testo)
    for word in mispelled:
        testo[testo.index(word)]=checker.correction(word)     
    
    badCount=0
    for line in profanities:
        if line.split('\n')[0] in " ".join(testo):
            badCount+=1
    
    return 100 - round((badCount/len(testo))*100, 2)

#for use miSpelling you HAVE TO install the SpellCheker library (https://pyspellchecker.readthedocs.io/en/latest/)
def miSpelling(testo):
    spell=SpellChecker()
    testo = cleanText(testo).split()
    misspelled= [el for el in spell.unknown(testo) if not '@' in el]
    return 100 - round((len(misspelled)/len(testo))*100,2)

def textCredibility(tweet_id, NLP=False, isSpam_weight=0.34, badWords_weight=0.33, miSpelling_weight=0.33):
    try:
        testo = getText(tweet_id)
    except:
        return None
    if NLP:
        return isSpam_weight*isSpamNLP(testo)+badWords_weight*badWords(testo)+miSpelling_weight*miSpelling(testo)
    else:
        return isSpam_weight*isSpamXGB(testo)+badWords_weight*badWords(testo)+miSpelling_weight*miSpelling(testo)

