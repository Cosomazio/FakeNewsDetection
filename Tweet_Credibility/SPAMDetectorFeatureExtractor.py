import re 
import emoji
import sys
import os
import string
import json
import csv
from tqdm import tqdm
#sys.path.insert(1, '../FakeNewsDetection/FNDetection/feature_extraction')
from feature_extraction.content_level import *
from feature_extraction.text_processing import *

def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    return testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()

def num_word(text):
  count = 0
  text=cleanText(text) 
  words=text.split()
  for word in words:
    count+=1
  return count

def text_len(text): #we count the character in according to count of twitter
    count = 0
    text = remove_mention(text)
    #print(text)
    for word in text:
        if emoji.is_emoji(word):
            count +=2
        else:
            count +=1
    return count

def num_of_usermention(text):
    text=text.split()
    count = 0
    for el in text:
        if "@" in el:
            el=el.split("@")
            for user in el[1:]:
                    count+=1
    return count

def num_of_tag(text):
    return len(find_all_hashtags(text))

def num_link(text):
    return len(find_all_urls(text))

def num_of_spamword(text):
    with open(os.path.realpath(os.path.dirname(__file__))+'/spamWords.txt', 'r') as spamDict:
        spam1 = spamDict.readlines()
    spam = list()
    for word in spam1:
        spam.append(word[:-1])

    spamCount=0
    testo = cleanText(text)
    #print(testo)
    for line in spam:
        #print(line.lower())
        if line.lower() in testo.lower():
            spamCount+=1
    return spamCount

def num_of_uppercase(text):
    count = 0
    
    text = clearText(text)
    text = text.replace(" ", "")
    for el in text:
        #print(el,el.upper())
        if el == el.upper() and not el.isnumeric():
            count +=1
    return count

def num_of_emoji(text):
    count = 0
    taken=[]
    for el in text:
        if emoji.is_emoji(el):
            #print("found")
            count+=1

    with open("./TweetCredibility/feature_extraction/resources/emoji_map.json", 'r') as file:
        emojis=json.load(file)
    #print(text.split())
    for el in emojis:
        if not el in taken: 
            for ch in text.split():
                if el in ch:
                #print(el,text)
                    taken.append(el)
                    count+=1
    return count

def num_spam_symb(text):
    count = 0
    for el in text:
        if el == "$" or el == "£" or el == "€":
            count +=1
    return count 

def features_extraction(text):
    featu=[]
    featu.append(num_of_emoji(text))
    featu.append(num_of_uppercase(text))
    featu.append(num_of_spamword(text))
    featu.append(num_of_tag(text))
    featu.append(num_link(text))
    featu.append(num_word(text))
    featu.append(text_len(text))
    featu.append(num_of_usermention(text))
    featu.append(num_spam_symb(text))
    #vedi se aggiungendo $ migliora
    return featu
    

if __name__ == "__main__":
    file_path="/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/materiale/spam_train2.csv"
    ids=[]
    row=[]
    with open(file_path,'r') as f:
        reader = csv.reader(f,delimiter="\t")
        #header = next(reader)
        for el in reader:
            ids.append(el)

    
    with open('TweetCredibility/spamFetature2.csv', 'a') as csvfile:
            row=[]
            writer = csv.writer(csvfile)
            for el in tqdm(ids):
                if len(el) < 2:
                    continue 
                row=features_extraction(el[1])
                if el[0] == "ham,":
                    row.append("1")
                else:
                    row.append("0")

                writer.writerow(row)
            