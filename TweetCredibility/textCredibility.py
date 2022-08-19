import json
import os
from nltk.tokenize import word_tokenize
import string
from spellchecker import SpellChecker


def getText(tweetPath):
    file = open(tweetPath)
    data = json.load(file)
    text = data['text']
    file.close()
    return text

def isSpam(testo):
    pass

def badWords(testo):
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(location, 'bad_words.txt'), 'r') as badDict:
        profanities= badDict.readlines()
    testo=testo.translate(str.maketrans('', '', string.punctuation))
    testo=testo.lower()

    badCount=0
    for line in profanities:
        if line.split('\n')[0] in testo:
            badCount+=1
    
    return round((badCount/len(testo.split()))*100, 2)

#for use miSpelling you HAVE TO install the SpellCheker library (https://pyspellchecker.readthedocs.io/en/latest/)
def miSpelling(testo):
    testo=testo.translate(str.maketrans('', '', string.punctuation))
    spell=SpellChecker()
    testo = testo.lower().split()
    misspelled=spell.unknown(testo)
    return round((len(misspelled)/len(testo))*100,2)

def textCredibility(tweetPath):
    testo = getText(tweetPath)
    return isSpam(testo)+badWords(testo)+miSpelling(testo)


stringa="my sweet, jesus f*ck i: love this plsanft because there are all thoae dicks"
print(badWords(stringa))
print(miSpelling(stringa))
