from content_level import *
from sentiment_analysis import *
from tweet_level import *
from user_level import *
from twitter_api import *
import time
import numpy as np
import pandas as pd
import numpy as np
import csv


def user_extraction(user, v2_conenction):
    #user_infos from twitter API
    def_profile = default_profile(user)
    follower_count = followers_count(user)
    friend_count = friends_count(user)
    prof_back_tile = profile_background_tile(user)
    prof_use_back_image = profile_use_background_image(user)
    status_count = statuses_count(user)

    #other user level_features
    desc_with_hashtags = desc_contains_hashtags(user)
    desc_with_user_mentions = desc_contains_user_mention(user, v2_conenction)
    desc_with_url = desc_contains_url(user)
    desc_len = desc_length(user)
    url_len = url_lenght (user)
    friends_p_follower = friends_per_followers(user)
    is_follow_more = is_following_more_than_100(user)
    days_ago = created_days_ago(user)

    return [def_profile, follower_count, friend_count, prof_back_tile, prof_use_back_image, status_count, 
    desc_with_hashtags, desc_with_user_mentions, desc_with_url, desc_len, url_len, friends_p_follower,is_follow_more, days_ago]
    
def tweet_extraction(tweet_status, tid, v2_connection):
    text = get_tweet_text(tweet_status)
    #tweet_infos from twitter API
    tweet_favourite_count =  favorite_count(tweet_status)
    possible_sensitive = possibly_sensitive(tweet_status)
    retweet_count = retweeted_count(tweet_status)
    trunc = truncated(tweet_status)

    #other tweet level_features
    numb_of_url = nr_of_urls(text)
    avg_url_len = avg_url_length(text)
    url_just = url_only(text)
    num_of_hashtags = nr_of_hashtag(text)
    nr_of_media = num_of_media(tid,  v2_connection)
    nr_of_user_mentions = num_of_usermention(text)
    nr_of_unicode_emoji = num_unicode_emoji(text)
    face_positive_emoji = contain_face_positive_emoji(text)
    face_negative_emoji = contain_face_negative_emoji(text)
    face_neutral_emoji = contain_face_neutral_emoji(text)
    nr_ascii_emoji = num_ascii_emoji(text)
    contain_stock_symbols = contains_stock_symbols(text)
    num_of_punctuation = nr_of_punctuation(text)
    ratio_punctuation_token = ratio_of_punctuation(text)
    nr_of_excalamation_marks = nr_of_exclamation_marks(text)
    num_of_question_marks = nr_of_question_marks(text)
    contains_character_repetitions = character_repetitions(text)

    return [tweet_favourite_count, possible_sensitive, retweet_count, trunc, numb_of_url, avg_url_len, url_just,
    num_of_hashtags, nr_of_media, nr_of_user_mentions, nr_of_unicode_emoji, face_positive_emoji, face_negative_emoji,
    face_neutral_emoji, nr_ascii_emoji, contain_stock_symbols, num_of_punctuation, ratio_punctuation_token,
    nr_of_excalamation_marks, num_of_question_marks, contains_character_repetitions]

def content_extraction(tweet_status):
    text = get_tweet_text(tweet_status)
    #content_level featrues
    contain_number = contains_number(text)
    contain_quote = contains_quotes(text)
    O_text = no_text(text) 
    avg_word_len = avg_word_length(text)
    text_len = text_length(text)
    nr_of_words = nr_words_token(text)
    nr_of_token = nr_of_tokens(text)
    all_uppercase = is_all_uppercase(text)
    contain_uppercase_text = contains_uppercase_text(text)
    ratio_capitalized_word = ratio_capitalized_words(text)
    ratio_all_capitalized_word = ratio_all_capitalized_words(text)
    nr_of_sentences = num_of_sentences(text)
    nr_of_slang_words = num_of_slang_words(text)
    ratio_adjective = ratio_adjectives(text)
    ratio_noun = ratio_nouns(text)
    ratio_verb = ratio_verbs(text)
    contains_pronoun = contains_pronouns(text)
    ratio_stopword = ratio_stopwords(text)
    contains_spelling_mistake = miSpelling(text)

    return [contain_number, contain_quote, O_text, avg_word_len, text_len, nr_of_words, nr_of_token, all_uppercase,
    contain_uppercase_text, ratio_capitalized_word, ratio_all_capitalized_word, nr_of_sentences,nr_of_slang_words,
    ratio_adjective, ratio_noun, ratio_verb, contains_pronoun, ratio_stopword, contains_spelling_mistake]

def sentiment_extraction(tweet_status):
    text = get_tweet_text(tweet_status)
    #sentiment_level features
    sentiment_value = sentiment_score(text)
    num_pos_sentiment_words = nr_pos_sentiment_words(text)
    num_neg_sentiment_words = nr_neg_sentiment_words(text)

    return [sentiment_value, num_pos_sentiment_words, num_neg_sentiment_words]

def extraction(tweet_ID, v2_connection, v1_connection):
     
    user = get_utente(tweet_ID, v2_connection, v1_connection)
    if(user == None):
        print("tweet not found")
        time.sleep(1)
        return None
    
    tweet_status = get_tweet_status(tweet_ID, v1_connection)

    return np.array(user_extraction(user, v2_connection) +  tweet_extraction(tweet_status, tweet_ID, v2_connection) + content_extraction(tweet_status)+ sentiment_extraction(tweet_status))
    

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
    with open("./train.csv", 'a') as f:
        writer = csv.writer(f)
        for i in (range(len(df_fake.index))):
            row = df_fake.iloc[i]
            sample = extraction(row['id'], v2_connection, v1_connection)
            if(sample is not None):
                sample = np.append(sample, -1)
                writer.writerow(sample)
                print(i)

    print("start real loading")
    with open("./train.csv", 'a') as f:
        writer = csv.writer(f)
        for i in (range(len(df_real.index))):
            row=df_real.iloc[i]
            sample = extraction(row["id"], v2_connection, v1_connection)
            if(sample is not None):
                sample = np.append(sample, 1)

                writer.writerow(sample)
                print(i)

    

    

        
    

    

    

    

    

    



    



