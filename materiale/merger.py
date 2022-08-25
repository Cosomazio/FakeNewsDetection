import pandas as pd
import re
import string

def cleanText(testo):
    #print(type(testo))
    testo=re.sub("http\S+", '',  str(testo))
    testo= testo.translate(str.maketrans('', '', string.punctuation.replace('@', ""))).lower()
    return testo

file_path1="./FakeNewsDetection/TweetCredibility/spam_train1.csv"
file_path2="./FakeNewsDetection/TweetCredibility/spam_train2.csv"

file1_df = pd.read_csv(file_path1, delimiter='\t', header=None)
file2_df = pd.read_csv(file_path2, delimiter='\t', header=None)

file2_df = file2_df.rename(columns={0:'SPAM', 1:'TEXT'})
file1_df = file1_df.rename(columns={0:'SPAM', 1:'TEXT'})

#file1_df=file1_df.sample(frac=1)
#file2_df=file2_df.sample(frac=1)

train_spam_df=file1_df.iloc[:]

train_spam_df=pd.concat([train_spam_df, file2_df.iloc[:]], ignore_index=True)

train_path="./FakeNewsDetection/TweetCredibility/train_spam_dataset.csv"
train_spam_df.to_csv(train_path, "\t", header=None, index=False)


"""file1_df.SPAM = file1_df.SPAM.apply(lambda s: True if s=='spam,' else False)
file1_df.TEXT = file1_df.TEXT.apply(lambda text: cleanText(text))

file2_df.SPAM = file1_df.SPAM.apply(lambda s: True if s=='spam,' else False)
file2_df.TEXT = file1_df.TEXT.apply(lambda text: cleanText(text))"""

