import numpy as np 
import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam, RMSprop

from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow import keras

#model = keras.models.load_model("modello")

file_path=os.path.realpath(os.path.dirname(__file__))+'/train_spam_dataset.csv'
#data = pd.read_csv(file_path)
data = pd.read_csv(file_path, delimiter='\t', header=None)
#data = data.drop(columns=['Id', 'following','followers','actions','is_retweet','location'])
data=data.rename(columns={0:'Type', 1:'Tweet'})

#print(data['Type'].value_counts()) # QUality 6153 Spam 5815
shorter_len = len(data[data['Type']=='spam,'])
longer_len = len(data[data['Type']=='ham,'])

shorter_index=data[data["Type"]=="spam,"].index
longer_index = data[data["Type"]=="ham,"].index

np.random.seed(42)
random_indices = np.random.choice(longer_index, size=shorter_len, replace=False) #sampling without replacement

undersample_index = np.concatenate([shorter_index, random_indices])
df=data.loc[undersample_index]
df=df.sample(frac=1, random_state=42)
df=df.reset_index()

df=df.drop(columns=['index'])

df.Type = df.Type.apply(lambda s: 1 if s=='spam,' else 0)

print("PORTO LO STEMMA")
stemmer = PorterStemmer()

vocabolario=[]

for testo in df['Tweet']:
    testo=str(testo)
    #tolgo i caratteri speciali e sostituisco con gli spazi
    testo = re.sub("[^a-zA-Z]"," ",testo)
    testo=testo.lower().split()

    testo=[stemmer.stem(words) for words in testo if words not in set(stopwords.words("english"))]

    testo = " ".join(testo)
    vocabolario.append(testo)

vocab_size=20000 #7000->15000
one_hot_doc=[one_hot(words, n=vocab_size) for words in vocabolario]

frase_len = 280
embedded_doc= pad_sequences(one_hot_doc, maxlen=frase_len, padding="pre")

print("FINE PREPARAZIONE")
extract_features=pd.DataFrame(data=embedded_doc)
target=df['Type']

df_final=pd.concat([extract_features, target], axis=1)

X=df_final.drop("Type", axis=1).to_numpy()
y=df_final['Type'].to_numpy()

print(X.shape, y.shape)
x_train, x_val, y_train, y_val = train_test_split(X, y, random_state=777, test_size=0.3)

print(x_train.shape, y_train.shape, x_val.shape, y_val.shape)

print("CREAZIONE E TRANING")
"""callback=keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, mode='min')
model=Sequential()
feature_num=280 #70
model.add(Embedding(input_dim=vocab_size, output_dim=feature_num, input_length=frase_len))
model.add(LSTM(units=512))
model.add(Dense(units=1,activation="sigmoid"))
model.compile(optimizer=RMSprop(0.003), loss="binary_crossentropy", metrics=["binary_accuracy"])#metrics=binary_crossentropy

model.fit(x_train, y_train, validation_data=(x_val, y_val),epochs = 10, batch_size=64, callbacks=[callback]) #Adam(0.003)
model.save("modello.h5")"""

model = keras.models.load_model("modello.h5")

preds=model.predict(x_val)
predictions=[]

conto_el=0
sum_el=0
for i in range(len(preds)):
    if(preds[i]>0.5):
        predictions.append(True)
    else:
        predictions.append(False)

for i in range(len(x_val)):
    if(predictions[i]):
        if(y_val[i]==1):
            conto_el+=1
    if(y_val[i]):
        sum_el+=1

frac_spam_messages_correctly_detected = conto_el/sum_el

#print(predictions==True)
"""conto=0
for i in range(len(preds)):
    if preds[i] ==True and y_val[i]==1:
        conto+=1"""

#frac_spam_messages_correctly_detected = np.sum((predictions == True) & (y_val==1)) / np.sum(y_val == 1)
print('Fraction Spam Correctly Detected on Validation: ', frac_spam_messages_correctly_detected)

test_path=os.path.realpath(os.path.dirname(__file__))+'/train.csv'
test_data=pd.read_csv(test_path)
#test_data=pd.read_csv(test_path, header=None, delimiter="\t")
test_data = test_data.drop(columns=['Id', 'following','followers','actions','is_retweet','location'])
#test_data=test_data.rename(columns={0:'Type', 1:'Tweet'})
test_data.Type=test_data.Type.apply(lambda s: 1 if s=='Spam' else 0)

test_preds=[]
"""for testo in test_data['Tweet']:
    for sentences in testo:
        sentences=nltk.sent_tokenize(testo)

        for sentence in sentences:
            testo=[stemmer.stem(words) for words in sentence if words not in set(stopwords.words("english"))]
            words = re.sub("[^a-zA-Z]"," ",sentence) 
            if words not in set(stopwords.words('english')):
                word=nltk.word_tokenize(words)
                word= " ".join(word)

    oneHot=[one_hot(word, n=vocab_size)]
    text=pad_sequences(oneHot, maxlen=frase_len, padding="pre")
    test_preds.append(True if model.predict(text)>0.5 else False)"""

for testo in test_data['Tweet']:
    #tolgo i caratteri speciali e sostituisco con gli spazi
    testo = re.sub("[^a-zA-Z]"," ",testo)
    testo=testo.lower().split()

    testo=[stemmer.stem(words) for words in testo if words not in set(stopwords.words("english"))]

    testo = " ".join(testo)
    oneHot=[one_hot(testo, n=vocab_size)]

    text=pad_sequences(oneHot, maxlen=frase_len, padding="pre")
    test_preds.append(True if model.predict(text)>0.5 else False)



conto_el=0
sum_el=0
y_test=test_data['Type'].to_numpy()
for i in range(len(test_preds)):
    if(test_preds[i]):
        if(y_test[i]==1):
            conto_el+=1
    if(y_test[i]):
        sum_el+=1

frac_spam_test_messages_correctly_detected = conto_el/sum_el
print("TEST performance: ", frac_spam_test_messages_correctly_detected)
print("TEST general accuracy", accuracy_score(y_test, test_preds))










