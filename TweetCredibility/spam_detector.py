import pandas as pd
import numpy as np
import string
import re

def cleanText(testo):
    testo=re.sub("http\S+", '',  testo)
    return testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()

def predict_text(testo, spam_bow, non_spam_bow, FRAC_SPAM_TEXT):
    valid_words=[word for word in testo if word in spam_bow]

    spam_prob = [spam_bow[word] for word in valid_words]
    non_spam_prob = [non_spam_bow[word] for word in valid_words]

    spam_score = sum([np.log(probability) for probability in spam_prob]) + np.log(FRAC_SPAM_TEXT)
    non_spam_score = sum([np.log(probability) for probability in non_spam_prob]) + np.log(1-FRAC_SPAM_TEXT)

    print('Spam Score: ', spam_score)
    print('Non-Spam Score: ',non_spam_score)

    return spam_score >= non_spam_score

def prepare_model(csv_path):
    spam_df = pd.read_csv(csv_path)
    spam_df = spam_df[['SPAM', 'TEXT']]
    spam_df.SPAM = spam_df.SPAM.apply(lambda s: True if s=='spam' else False)

    spam_df.TEXT = spam_df.TEXT.apply(lambda text: cleanText(text))

    spam_df = spam_df.sample(frac=1, random_state=42)