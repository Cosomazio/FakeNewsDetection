from content_level import *
from sentiment_analysis import *
from tweet_level import *
from user_level import *
from twitter_api import *
import numpy as np

def user_extraction(uid, v1_connection, v2_connection):
    #user_infos from twitter API
    def_profile = default_profile(uid, v1_connection)
    follower_count = followers_count(uid, v2_connection)
    friend_count = friends_count(uid, v2_connection)
    prof_back_tile = profile_background_tile(uid, v1_connection)
    prof_use_back_image = profile_use_background_image(uid, v1_connection)
    status_count = statuses_count(uid, v2_connection)

    #other user level_features
    has_descrip = has_desc(uid, v2_connection)
    desc_with_hashtags = desc_contains_hashtags(uid, v2_connection)
    desc_with_user_mentions = desc_contains_user_mention(uid, v2_connection)
    desc_with_url = desc_contains_url(uid, v2_connection)
    desc_len = desc_length(uid, v2_connection)
    url_len = url_lenght (uid, v2_connection)
    friends_p_follower = friends_per_followers(uid, v2_connection)
    is_follow_more = is_following_more_than_100(uid, v2_connection)
    days_ago = created_days_ago(uid, v2_connection)

    return [def_profile, follower_count, friend_count, prof_back_tile, prof_use_back_image, status_count,has_descrip, 
    desc_with_hashtags, desc_with_user_mentions, desc_with_url, desc_len, url_len, friends_p_follower,is_follow_more, days_ago]
    
def tweet_extraction(text, tid, v1_connection, v2_connection):
    #tweet_infos from twitter API
    tweet_favourite_count =  favorite_count(tid, v1_connection)
    possible_sensitive = possibly_sensitive(tid, v1_connection)
    retweet_count = retweeted_count(tid, v1_connection)
    trunc = truncated(tid, v1_connection)

    #other tweet level_features
    numb_of_url = nr_of_urls(text)
    avg_url_len = avg_url_length(text)
    url_just = url_only(text)
    num_of_hashtags = nr_of_hashtag(text)
    nr_of_media = num_of_media(tid,  v2_connection)
    nr_of_user_mentions = num_of_usermention(text, v2_connection)
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

def content_extraction(text):
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

def sentiment_extraction(text):
    #sentiment_level features
    sentiment_value = sentiment_score(text)
    num_pos_sentiment_words = nr_pos_sentiment_words(text)
    num_neg_sentiment_words = nr_neg_sentiment_words(text)

    return [sentiment_value, num_pos_sentiment_words, num_neg_sentiment_words]

def extraction(tweet_ID, user_ID=None):
    v2_connection = api_v2_connection()
    v1_connection = api_v1_connection()
    if user_ID == None:
        uid=get_user_id(tweet_ID, v2_connection)
    else:
        uid = user_ID
    
    text = get_tweet_text(tweet_ID, v1_connection)

    return np.array(user_extraction(uid, v1_connection, v2_connection) +  tweet_extraction(text, tweet_ID, v1_connection, v2_connection) + content_extraction(text)+ sentiment_extraction(text))
    
    
    

    

    

    

    

    



    



