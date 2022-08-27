import json
import os
import re
import string
from spellchecker import SpellChecker
from spamdetectorNLP import predictText
#from spamdetectorLSTM import predictText

def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    return testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()
    
def getText(tweetPath):
    file = open(tweetPath)
    data = json.load(file)
    text = data['text']
    file.close()
    return text

def isSpamNLP(testo):
    return 0 if predictText(testo) else 100

"""def isSpamLSTM(testo):
    return 100 - round(predictText(testo), 2)*100"""

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

def textCredibility(tweetPath, NLP=True, isSpam_weight=0.34, badWords_weight=0.33, miSpelling_weight=0.33):
    testo = getText(tweetPath)
    if NLP:
        return isSpam_weight*isSpamNLP(testo)+badWords_weight*badWords(testo)+miSpelling_weight*miSpelling(testo)
