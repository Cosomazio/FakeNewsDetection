import pandas as pd
import numpy as np
import string
import re
import os

def cleanText(testo):
    #print(type(testo))
    testo=re.sub("http\S+", '',  str(testo))
    testo= testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()
    return testo

def predict_text(testo, spam_bow, non_spam_bow, FRAC_SPAM_TEXT):
    valid_words=[word for word in testo if word in spam_bow]

    spam_prob = [spam_bow[word] for word in valid_words]
    non_spam_prob = [non_spam_bow[word] for word in valid_words]

    spam_score = sum([np.log(probability) for probability in spam_prob]) + np.log(FRAC_SPAM_TEXT)
    non_spam_score = sum([np.log(probability) for probability in non_spam_prob]) + np.log(1-FRAC_SPAM_TEXT)

    print(abs(spam_score-non_spam_score))
    return spam_score >= non_spam_score

def prepare_dataframe(csv_path):
    spam_df = pd.read_csv(csv_path, delimiter='\t', header=None)
    spam_df = spam_df.rename(columns={0:'SPAM', 1:'TEXT'})
    
    spam_df.SPAM = spam_df.SPAM.apply(lambda s: True if s=='spam,' else False)
    spam_df.TEXT = spam_df.TEXT.apply(lambda text: cleanText(text))
    spam_df = spam_df.sample(frac=1, random_state=23)

    train_spam_df=spam_df.iloc[:int(len(spam_df)*0.8)]
    val_spam_df=spam_df.iloc[int(len(spam_df)*0.8):]

    FRAC_SPAM_TEXTS = train_spam_df.SPAM.mean()
    FRAC_SPAM_TEXT1 = val_spam_df.SPAM.mean()
    print(FRAC_SPAM_TEXTS, FRAC_SPAM_TEXT1)

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

def test_performance(test_path, spam_bow, non_spam_bow, FRAC_SPAM_TEXTS):
    test_df = pd.read_csv(test_path)
    test_df=test_df.rename(columns={'label':'SPAM', 'message':'TEXT'})

    test_df.SPAM = test_df.SPAM.apply(lambda s: True if s==1 else False)
    test_df.TEXT = test_df.TEXT.apply(lambda text: cleanText(text))

    test_pred=test_df.TEXT.apply(lambda text: predict_text(text.split(), spam_bow, non_spam_bow, FRAC_SPAM_TEXTS))

    correctly_detected = np.sum((test_pred == True) & (test_df.SPAM == True)) / np.sum(test_df.SPAM == True)
    return correctly_detected


if __name__ == '__main__':
    file_path=os.path.realpath(os.path.dirname(__file__))+'/train_spam_dataset.csv'
    test_path=os.path.realpath(os.path.dirname(__file__))+'/messages.csv'
    train_spam_df, val_spam_df, FRAC_SPAM_TEXTS=prepare_dataframe(file_path)
    spam_bow, non_spam_bow = create_bag_of_words(train_spam_df)

    predictions = val_spam_df.TEXT.apply(lambda t: predict_text(t.split(), spam_bow, non_spam_bow, FRAC_SPAM_TEXTS))
    frac_spam_messages_correctly_detected = np.sum((predictions == True) & (val_spam_df.SPAM == True)) / np.sum(val_spam_df.SPAM == True)
    print('Fraction Spam Correctly Detected on Validation: ', frac_spam_messages_correctly_detected)
    print('Fraction Spam Correctly Detected on TEST: ', test_performance(test_path, spam_bow, non_spam_bow, FRAC_SPAM_TEXTS))



