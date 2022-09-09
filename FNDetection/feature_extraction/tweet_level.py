import re
import string
import json
from content_level import *
from twitter_api import api_v2_connection

def nr_of_urls(text):
    """takes the text of a tweet and return the number of urls"""
    return len(find_all_urls(text))

def avg_url_length(text):
    """returns the average url length"""
    urls = find_all_urls(text)
    if len(urls) == 0:
        return 0
    somma=0
    for url in urls:
        somma+=len(url)
    return round(somma/len(urls), 2)

def url_only(text):
    """verify if the text of a tweet is made by urls only"""
    if(len(text) == 0):
        return False
    text=remove_urls(text)
    text=re.sub('[^A-Za-z0-9]+', '', text) 
    if(len(text)==0):
        return True
    return False

def nr_of_hashtag(text):
    """ counts the number of hashtags in the text"""
    return len(find_all_hashtags(text))

def nr_of_popular_hashtag(text):
    pass

def nr_of_punctuation(text):
    """returns the number of punctuation characters used in the actual text of a tweet"""
    punteggiatura = list(string.punctuation) + ['’', '…', '‘', '“', '”']
    somma=0

    no_url=remove_urls(text)
    if(len(no_url)==0):
        return 0
    for carattere in no_url:
        if carattere in punteggiatura:
            somma+=1
    return somma

def ratio_of_punctuation(text):
    #la lunghezza della strigna tiene in considerazione anche gli spazi bianchi: tokenizzare per verificare punteggiatura rispetto a soli caratteri utili o meno?
    """ ratio of punctuation characters respect to the length of the string"""
    text=remove_urls(text)
    if(len(text)==0):
        return 0
    somma=nr_of_punctuation(text)
    print(somma, len(tokenization(text)), tokenization(text))
    return round(somma/len(tokenization(text)), 3)

def nr_of_exclamation_marks(text):
    """ counts the number of exclamation marks that are present in the string"""
    somma=0
    for carattere in remove_urls(text):
        if carattere == '!':
            somma+=1
    return somma

def nr_of_question_marks(text):
    """ counts the number of question marks that are present in the string"""
    somma=0
    for carattere in remove_urls(text):
        if carattere == '?':
            somma+=1
    return somma

def contains_stock_symbols(text):
    """finds stock mentions in the text (all words that start with $)"""
    stocks = []
    words = text.split()
    for w in words:
        if len(w) > 0:
            if re.match("\$\w+", w):
                stocks.append(w)
    return len(stocks) > 0

def character_repetitions(text):
    """ returns True if a character is followed by at least 2 repetitions of itself """
    pattern = re.compile(r"(.)\1{2,}")
    if re.findall(pattern, text):
        return True
    else:
        return False

def num_ascii_emoji(text):
    count = 0
    checked_emoji=list()
    filepath="FNDetection/feature_extraction/resources/ascii_emojis.json"
    with open(filepath,'r') as f:
        data = json.load(f)
    for emoji in data:
        #print(emoji)
        if emoji in checked_emoji:
            continue
        else:
            checked_emoji.append(emoji)
            if emoji in text:
                #print(emoji)
                count+=1
    return count

def contain_face_positive_emoji(text):
    filepath="FNDetection/feature_extraction/resources/emoji_map.json"
    with open(filepath,'r') as f:
        data = json.load(f)

    for emoji in data["face-positive"]:
        for word in text:
            word = 'U+{:X}'.format(ord(word))
            if emoji in word:
                return True
    return False

def contain_face_negative_emoji(text):
    filepath="FNDetection/feature_extraction/resources/emoji_map.json"
    with open(filepath,'r') as f:
        data = json.load(f)
    for emoji in data["face-negative"]:
        for word in text:
            word = 'U+{:X}'.format(ord(word))
            if emoji in word:
                return True
    return False

def contain_face_neutral_emoji(text):
    filepath="FNDetection/feature_extraction/resources/emoji_map.json"
    with open(filepath,'r') as f:
        data = json.load(f)
    for emoji in data["face-neutral"]:
        for word in text:
            word = 'U+{:X}'.format(ord(word))
            if emoji in word:
                return True
    return False

def num_unicode_emoji(text):
    count = 0
    filepath="FNDetection/feature_extraction/resources/emoji_map.json"
    with open(filepath,'r') as f:
        data = json.load(f)
    for el in data:
        for emoji in data[el]:
            for word in text:
                word = 'U+{:X}'.format(ord(word))
                if emoji in word:
                    count+=1
    return count

def num_of_media(tweet_id):
    """return the num of media in the tweet"""
    connection = api_v2_connection()
    tweet = connection.get_tweet(tweet_id,tweet_fields=["attachments"])
    return len(tweet.data.attachments["media_keys"])

def num_of_usermention(text):
    """return the num of usermention"""
    count = 0
    text = text.split()
    for el in text:
        if '@' in el:
            username=el.split("@")[-1]
            client = api_v2_connection()
            user = client.get_user(username=username)
            #print(user.data)
            if user.data != None : count+=1
    return count


if __name__=="__main__":
    text="@playbingobash Gems are sparkling everywhere! in #BingoBash!!! http://bash.gg/1Y35AQ0"

    print("nr_of_#: ", nr_of_hashtag(text))
    print("nr_of_punctuation: ", nr_of_punctuation(text))
    print("ratio of punctuation: ", ratio_of_punctuation(text))
    print("character_repetitions: ", character_repetitions(text))
    print("stock_symbols: ", contains_stock_symbols(text))
    print("nr of exclamation marks: ", nr_of_exclamation_marks(text))
    print("nr of question marks: ", nr_of_question_marks(text))
    #print("avg_url_length: ", avg_url_length(text))
    #print("url_only: ", url_only(text))


    
    print(contain_face_positive_emoji("😊😟🙁😡🙂😑❤️"))
    print(contain_face_negative_emoji("😞"))
    print(contain_face_neutral_emoji("😊😟🙁😡🙂😑❤️"))
    print(num_unicode_emoji("😊😟🙁🙂😑"))


    print(num_ascii_emoji(":( :-) "))
    print(num_of_usermention("#Ampadu from @ChelseaFC to @acspezia ⏳ Loan with option to buy (€15m). He'll undergo medicals on Tuesday. #CFC #Chelsea #transfers @SkySport @SkySports"))
        
