from feature_extraction.content_level import *
from feature_extraction.tweet_level import *
from feature_extraction.user_level import *
from feature_extraction.twitter_api import *

def check_tweet(tweet_id,v2_connection):
    tweet = v2_connection.get_tweet(id=tweet_id)
    return 0 if str(tweet.data) == "None" else 1

def contains_questionmark(text):
    """contains ?"""
    return 1 if nr_of_question_marks(text) > 0 else 0

def contains_exclamationpoint(text):
    """contains !"""
    return 1 if nr_of_exclamation_marks(text) > 0 else 0

def contains_multi_qe(text):
    """contains multiple ? or !"""
    return 1 if nr_of_question_marks(text) > 1 or nr_of_exclamation_marks(text) > 1 else 0

def contains_dollar(text):
    """contains $"""
    for el in text:
        if el == "$":
            return 1
    return 0

def contains_url(text):
    return 1 if nr_of_urls(text) > 0 else 0

def contains_media(tweet_id,v2_connection):
    return 1 if num_of_media(tweet_id,v2_connection) > 0 else 0

def contains_hashtags(text):
    return 1 if nr_of_hashtag(text) > 0 else 0

def contains_mention(text):
    return 1 if num_of_usermention(text) > 0 else 0

def registration_age(user):
    if hasattr(user, "created_at"):
        return str(user.created_at).split()[0]
    else: return 0

def default_profile_img(user):
    if hasattr(user, "default_profile_image"):
        return user.default_profile_image
    else: return 0

def feature_extractions(tweet_id,tweet_text,user,v2_connection, v1_connection):
    feature=[]
    if user == None:
        return None
    
    feature.append(text_length(tweet_text))
    feature.append(nr_words_token(tweet_text))

    feature.append(contains_questionmark(tweet_text))
    feature.append(contains_exclamationpoint(tweet_text))
    feature.append(contains_multi_qe(tweet_text))

    feature.append(nr_of_urls(tweet_text))
    feature.append(contains_url(tweet_text))
    feature.append(contains_media(tweet_id,v2_connection))
    feature.append(contains_hashtags(tweet_text))
    feature.append(contains_dollar(tweet_text))
    feature.append(contains_mention(tweet_text))

    feature.append(registration_age(user))
    feature.append(statuses_count(user))
    feature.append(followers_count(user))
    feature.append(friends_count(user))
    feature.append(verified(user))
    feature.append(desc_length(user))
    feature.append(desc_contains_url(user))
    feature.append(default_profile(user))
    feature.append(default_profile_img(user))
    feature.append(profile_use_background_image(user))
    return feature