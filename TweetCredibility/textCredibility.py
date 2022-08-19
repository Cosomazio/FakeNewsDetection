import json
import os
import re
import string
from spellchecker import SpellChecker

def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    return testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()


def getText(tweetPath):
    file = open(tweetPath)
    data = json.load(file)
    text = data['text']
    file.close()
    return text

def isSpam(testo):
    pass

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
    
    return round((badCount/len(testo))*100, 2)

#for use miSpelling you HAVE TO install the SpellCheker library (https://pyspellchecker.readthedocs.io/en/latest/)
def miSpelling(testo):
    spell=SpellChecker()
    testo = cleanText(testo).split()
    misspelled= [el for el in spell.unknown(testo) if not '@' in el]
    return round((len(misspelled)/len(testo))*100,2)

def textCredibility(tweetPath):
    testo = getText(tweetPath)
    print(badWords(testo))
    print(miSpelling(testo))
    #return isSpam(testo)+badWords(testo)+miSpelling(testo)


tweetpath="./FakeNewsDetection/TweetCredibility/529572620782825473.json"
textCredibility(tweetpath)
