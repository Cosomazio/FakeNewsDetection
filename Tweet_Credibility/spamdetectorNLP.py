from turtle import st
import pandas as pd
import numpy as np
import string
import re
import os
from emoji import is_emoji #pip install emoji


#Commento

def max_count_uppercase(text, maxCount=5):
    count_upp=0
    words= text.split()
    for word in words:
        #print(word)
        if word == word.upper():
            count_upp+=1
    #ritorno 100 se il conteggio è superiore della soglia impostata dall'user 
    return 100 if count_upp >= maxCount else 0


def containslink(text):
    #extractor = URLExtract()
    # url = extractor.find_urls(text)
    # if len(url) != 0:
    #         return True
    if "http" in text:
        #print(word)
        return True
    return False

def max_count_emoji(text,maxCount=10):
    count_emoji = 0
    for word in text:
        if is_emoji(word):
            count_emoji += 1
    return 100 if count_emoji >= maxCount else 0

def max_count_punctuation(text,maxCount=50):
    count_punct=0
    for word in text:
        #print(word)
        if word in string.punctuation:
            count_punct +=1
    if count_punct >= maxCount:
        return 100
    else:
        return 0

def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    testo=re.sub("https\S+", '',  testo)
    for c in string.punctuation:
        if c != '£' and c != '$' and c != '!':
            testo = testo.replace(c,'')
    return testo
    
def contains_spam_word(testo):
    #print("controlla",testo)
    with open(os.path.realpath(os.path.dirname(__file__))+'/spamWords.txt', 'r') as spamDict:
        spam1 = spamDict.readlines()
    spam = list()
    for word in spam1:
        spam.append(word[:-1])

    spamCount=0
    testo = cleanText(testo)
    #print(testo)
    for line in spam:
        #print(line.lower())
        if line.lower() in testo.lower():
            spamCount+=1
    
    return 100 if spamCount != 0 else 0

def predictText(text,maxCountUppercase=3,maxCountEmoji=10,maxCountPunctuation=30):
    text=str(text)
    if contains_spam_word(text):
        return True
    elif containslink(text):
        return True
    elif max_count_uppercase(text,maxCountUppercase) == 100:
        return True
    elif max_count_punctuation(text,maxCountPunctuation) == 100:
        return True
    elif max_count_emoji(text,maxCountEmoji) == 100:
        return True
    else:
        return False



if __name__ == '__main__':

    filepath1=os.path.realpath(os.path.dirname(__file__))+'/train_spam_dataset.csv'
    filepath = os.path.realpath(os.path.dirname(__file__))+'/train.csv'

    spam_df1 = pd.read_csv(filepath1, delimiter='\t', header=None)
    spam_df1 = spam_df1.rename(columns={0:'SPAM', 1:'TEXT'})
    spam_df1.SPAM = spam_df1.SPAM.apply(lambda s: True if s=='spam,' else False)
    
    #############################################
    data = pd.read_csv(filepath)
    data = data.drop(columns=['Id', 'following','followers','actions','is_retweet','location'])
    
    spam_df = data.rename(columns={"Type":'SPAM', "Tweet":'TEXT'})
    spam_df.SPAM = spam_df.SPAM.apply(lambda s: True if s=='Spam' else False)

    #############################################

    predictions1 = spam_df1.TEXT.apply(lambda t: predictText(t))
    frac_spam_messages_correctly_detected = np.sum((predictions1 == True) & (spam_df1.SPAM == True))
    frac_nospam = np.sum((predictions1 == False) & (spam_df1.SPAM == False))
    pred = (frac_nospam+frac_spam_messages_correctly_detected) / len(spam_df1.SPAM)
    
    frac_spam_messages_correctly_detected = np.sum((predictions1 == True) & (spam_df1.SPAM == True)) / np.sum(spam_df1.SPAM == True)
    frac_nospam = np.sum((predictions1 == False) & (spam_df1.SPAM == False)) / np.sum(spam_df1.SPAM == False)

    print('Fraction Spam Correctly Detected ', pred,frac_spam_messages_correctly_detected,frac_nospam)

    predictions = spam_df.TEXT.apply(lambda t: predictText(t))
    frac_spam_messages_correctly_detected = np.sum((predictions == True) & (spam_df.SPAM == True)) 
    frac_nospam = np.sum((predictions == False) & (spam_df.SPAM == False))
    
    pred = (frac_nospam+frac_spam_messages_correctly_detected) / len(spam_df.SPAM)

    frac_spam_messages_correctly_detected = np.sum((predictions == True) & (spam_df.SPAM == True)) / np.sum(spam_df.SPAM == True)
    frac_nospam = np.sum((predictions1 == False) & (spam_df1.SPAM == False)) / np.sum(spam_df.SPAM == False)
    print('Fraction Spam Correctly Detected ', pred,frac_spam_messages_correctly_detected,frac_nospam)


