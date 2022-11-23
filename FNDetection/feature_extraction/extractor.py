from feature_extraction.content_level import *
from feature_extraction.tweet_level import *
from feature_extraction.user_level import *
from feature_extraction.twitter_api import *
import time
import numpy as np
import pandas as pd
import numpy as np
import csv

""" this function extracts all the user-related features"""
def user_extraction(user, v2_conenction):
    #user_infos from twitter API
    def_profile = default_profile(user)
    follower_count = followers_count(user)
    friend_count = friends_count(user)
    prof_use_back_image = profile_use_background_image(user)
    status_count = statuses_count(user)

    #other user level_features
    desc_with_url = desc_contains_url(user)
    desc_len = desc_length(user)
    days_ago = created_days_ago(user)
    verif = verified(user)
    def_prof_img = default_profile_img(user)

    return [days_ago, status_count, follower_count, friend_count, verif, desc_len, desc_with_url, def_profile, def_prof_img, prof_use_back_image]

"""extracts all the tweet-related features"""
def tweet_extraction(tweet_status, tid, v2_connection):
    text = get_tweet_text(tweet_status)
    #tweet_infos from twitter API

    #other tweet level_features
    numb_of_url = nr_of_urls(text)
    cont_url = contains_url(text)
    cont_hashtags = contains_hashtags(text)
    cont_media = contains_media(tid,  v2_connection)
    cont_mentions = contains_mention(text)
    cont_of_excalamation_marks = contains_exclamations_marks(text)
    cont_of_question_marks = contains_question_marks(text)
    cont_multi_q_e = contains_multi_q_e(text)
    contains_dollar = contains_stock_symbols(text)

    return [cont_of_question_marks, cont_of_excalamation_marks, cont_multi_q_e, numb_of_url, cont_url, cont_media, cont_hashtags, contains_dollar, cont_mentions]

"""extracts all the content-related features"""
def content_extraction(tweet_status):
    text = get_tweet_text(tweet_status)
    #content_level featrues
    text_len = text_length(text)
    nr_of_words = nr_words_token(text)

    return [text_len, nr_of_words]

""" given a Tweet ID return the corresponding feature vector"""
def extraction(tweet_ID, v2_connection, v1_connection):
    user = get_utente(tweet_ID, v2_connection, v1_connection)
    if(user == None):
        print("tweet not found")
        time.sleep(1)
        return None
    
    tweet_status = get_tweet_status(tweet_ID, v1_connection)
    
    userf = (user_extraction(user, v2_connection))
    tweetf = tweet_extraction(tweet_status, tweet_ID, v2_connection)
    contentf =content_extraction(tweet_status)
    return np.array(contentf + tweetf+ userf)
    

""" used to generate the test set from genuine and fake tweets"""
if __name__ == "__main__":
    path_fake = "./Sample/fake.csv"
    path_real = "./Sample/genuine.csv"

    df_fake = pd.read_csv(path_fake)
    df_real = pd.read_csv(path_real)
    data=[]
    labels=[]

    v2_connection = api_v2_connection()
    v1_connection = api_v1_connection()

    print("start fake loading")
    with open("./test1.csv", 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for i in (range(len(df_fake.index))):
            row = df_fake.iloc[i]
            sample = extraction(row['id'], v2_connection, v1_connection)
            if(sample is not None):
                sample = np.append(sample, -1)
                writer.writerow(sample)
                print(i)

    print("start real loading")
    with open("./test1.csv", 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for i in (range(len(df_real.index))):
            row=df_real.iloc[i]
            sample = extraction(row["id"], v2_connection, v1_connection)
            if(sample is not None):
                sample = np.append(sample, 1)

                writer.writerow(sample)
                print(i)