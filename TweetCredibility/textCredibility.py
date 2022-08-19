import json
import os
from nltk.tokenize import word_tokenize
import string

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
    testo=testo.translate(str.maketrans('', '', string.punctuation))
    testo=testo.lower()
    badCount=0
    for line in profanities:
        if line.split('\n')[0] in testo:
            badCount+=1
    
    return round((badCount/len(testo.split()))*100, 2)

def miSpelling(testo):
    pass

def textCredibility(tweetPath):
    testo = getText(tweetPath)
    return isSpam(testo)+badWords(testo)+miSpelling(testo)


stringa="my sweet, jesus fuck i: love this planet because there are all those dicks"
print(badWords(stringa))
