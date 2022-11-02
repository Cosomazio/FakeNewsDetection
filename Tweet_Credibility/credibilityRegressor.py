import sys
import numpy as np
import pickle
from feature_extraction.twitter_api import get_utente

from feature_extraction.twitter_api import api_v1_connection, api_v2_connection
from textCredibility import getText
from featureextraction import feature_extractions
import time
from datetime import date
import datetime

def convert_data(dates):
    date_format= "%Y-%m-%d"
    date_today=time.strptime(str(date.today()),date_format)
    date_today = datetime.datetime.fromtimestamp(time.mktime(date_today)) 
    date_created=time.strptime(dates,date_format)
    date_created = datetime.datetime.fromtimestamp(time.mktime(date_created))
    return (date_today-date_created).days

def features(tweet_id):
    feat = []
    v2_connection=api_v2_connection()
    v1_connection=api_v1_connection()
    tweet_text = getText(tweet_id)
    user = get_utente(tweet_id,v2_connection,v1_connection)
    feat= feature_extractions(tweet_id,tweet_text,user,v2_connection,v1_connection)
    for el in range(len(feat)):
        if feat[el] == False:
            #print(feat[el])
            feat[el]=0.0
        elif feat[el] == True:
            #print(feat[el])
            feat[el]=1.0
    feat[11]=convert_data(feat[11])   
    #print(feat)
    return feat

def credibility_score(tweet_id):
    X_test = features(tweet_id)
    x_test = np.array(X_test,dtype="float").reshape((1,21))

    model = pickle.load(open("./TweetCredibility/regressor",'rb'))
    
    y_pred = model.predict(x_test)
    return y_pred
    
if __name__ == "__main__":
    id = sys.argv
    print(credibility_score(id[-1])[0])
    
    