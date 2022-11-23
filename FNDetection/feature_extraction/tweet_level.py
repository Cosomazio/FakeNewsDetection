import re
import string
import json
from feature_extraction.content_level import *
from nltk.tokenize import word_tokenize

def nr_of_urls(text):
    """takes the text of a tweet and return the number of urls"""
    return len(find_all_urls(text))

def contains_url(text):
    return 1 if nr_of_urls(text)>0 else 0


def __nr_of_hashtag(text):
    """ counts the number of hashtags in the text"""
    return len(find_all_hashtags(text))

def contains_hashtags(text):
    return 1 if __nr_of_hashtag(text)>0 else 0

def __nr_of_exclamation_marks(text):
    """ counts the number of exclamation marks that are present in the string"""
    somma=0
    for carattere in remove_urls(text):
        if carattere == '!':
            somma+=1
    return somma

def contains_exclamations_marks(text):
    return 1 if len(__nr_of_exclamation_marks(text))>0 else 0

def __nr_of_question_marks(text):
    """ counts the number of question marks that are present in the string"""
    somma=0
    for carattere in remove_urls(text):
        if carattere == '?':
            somma+=1
    return somma

def contains_question_marks(text):
    return 1 if len(__nr_of_question_marks(text))>0 else 0

def contains_multi_q_e(text):
    1 if __nr_of_question_marks(text) > 1 or __nr_of_exclamation_marks(text) > 1 else 0

def contains_stock_symbols(text):
    """finds stock mentions in the text (all words that start with $)"""
    """contains $"""
    for el in text:
        if el == "$":
            return 1
    return 0

def __num_of_media(tweet_id, v2_connection):
    """return the num of media in the tweet"""
    connection = v2_connection
    tweet = connection.get_tweet(tweet_id,tweet_fields=["attachments"])
    if hasattr(tweet.data.attachments, "media_keys"):
        return len(tweet.data.attachments["media_keys"])
    else:
        return 0

def contains_media(tweet_id, v2_connection):
    return 1 if len(__num_of_media(tweet_id, v2_connection)) > 0 else 0

def __num_of_usermention(text):
    """return the num of usermention"""
    count = 0
    text = text.split()
    for el in text:
        if '@' in el:
            splitted = el.split("@")
            splitted = [el for el in splitted if el != ""]
            if len(splitted)==0:
                return 0
            username=word_tokenize(splitted[-1])[0]
            if username!= "" : count+=1
    return count

def contains_mention(text):
    return 1 if len(__num_of_usermention(text))>0 else 0

if __name__=="__main__":
    text="@playbingobash Gems are sparkling everywhere! in #BingoBash!!! http://bash.gg/1Y35AQ0"

    #print("nr_of_#: ", nr_of_hashtag(text))
    #print("nr_of_punctuation: ", nr_of_punctuation(text))
    #print("ratio of punctuation: ", ratio_of_punctuation(text))
    #print("character_repetitions: ", character_repetitions(text))
    #print("stock_symbols: ", contains_stock_symbols(text))
    #print("nr of exclamation marks: ", nr_of_exclamation_marks(text))
    #print("nr of question marks: ", nr_of_question_marks(text))
    #print("avg_url_length: ", avg_url_length(text))
    #print("url_only: ", url_only(text))


    
    #print(contain_face_positive_emoji("😊😟🙁😡🙂😑❤️"))
    #print(contain_face_negative_emoji("😞"))
    #print(contain_face_neutral_emoji("😊😟🙁😡🙂😑❤️"))
    #print(num_unicode_emoji("😊😟🙁🙂😑"))
    #print(num_ascii_emoji(":( :-) "))
    #print(num_of_usermention("#Ampadu from @ChelseaFC to @acspezia ⏳ Loan with option to buy (€15m). He'll undergo medicals on Tuesday. #CFC #Chelsea #transfers @SkySport @SkySports"))
