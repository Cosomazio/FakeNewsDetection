import pandas as pd
import numpy as np
import string
import re
import os

def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    return testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()

def predict_text(testo, spam_bow, non_spam_bow, FRAC_SPAM_TEXT):
    valid_words=[word for word in testo if word in spam_bow]

    spam_prob = [spam_bow[word] for word in valid_words]
    non_spam_prob = [non_spam_bow[word] for word in valid_words]

    spam_score = sum([np.log(probability) for probability in spam_prob]) + np.log(FRAC_SPAM_TEXT)
    non_spam_score = sum([np.log(probability) for probability in non_spam_prob]) + np.log(1-FRAC_SPAM_TEXT)

    #print('Spam Score: ', spam_score)
    #print('Non-Spam Score: ',non_spam_score)

    return spam_score >= non_spam_score

def prepare_dataframe(csv_path):
    spam_df = pd.read_csv(csv_path, delimiter='\t', header=None)

    spam_df = spam_df.rename(columns={0:'SPAM', 1:'TEXT'})
    

    spam_df.SPAM = spam_df.SPAM.apply(lambda s: True if s=='spam,' else False)

    spam_df.TEXT = spam_df.TEXT.apply(lambda text: cleanText(text))

    spam_df = spam_df.sample(frac=1, random_state=28)

    train_spam_df=spam_df.iloc[:int(len(spam_df)*0.8)]
    val_spam_df=spam_df.iloc[int(len(spam_df)*0.8):]

    FRAC_SPAM_TEXTS = train_spam_df.SPAM.mean()

    return train_spam_df, val_spam_df, FRAC_SPAM_TEXTS

def create_bag_of_words(train_spam_df):
    spam_words = ' '.join(train_spam_df[train_spam_df.SPAM == True].TEXT).split()
    non_spam_words = ' '.join(train_spam_df[train_spam_df.SPAM == False].TEXT).split()
    common_words = set(spam_words).intersection(set(non_spam_words))

    spam_bow = dict()
    non_spam_bow = dict()

    for word in common_words:
        spam_bow[word] = spam_words.count(word)/len(spam_words)
        non_spam_bow[word] = non_spam_words.count(word)/len(non_spam_words)
    
    return spam_bow, non_spam_bow



file_path=os.path.realpath(os.path.dirname(__file__))+'/train_datasetspam.csv'
train_spam_df, val_spam_df, FRAC_SPAM_TEXT=prepare_dataframe(file_path)
spam_bow, non_spam_bow = create_bag_of_words(train_spam_df)

predictions = val_spam_df.TEXT.apply(lambda t: predict_text(t.split(), spam_bow, non_spam_bow, FRAC_SPAM_TEXT))
frac_spam_messages_correctly_detected = np.sum((predictions == True) & (val_spam_df.SPAM == True)) / np.sum(val_spam_df.SPAM == True)
print('Fraction Spam Correctly Detected: %s'%frac_spam_messages_correctly_detected)



