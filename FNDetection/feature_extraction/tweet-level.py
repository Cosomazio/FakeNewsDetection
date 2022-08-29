import re
import string

def find_all_urls(text):
        """searches the text for urls and returns them"""
        search_str = '(?P<url>https?://[^\s]+)'
        result = re.findall(search_str, text)
        return result

def remove_urls(text):
        """removes urls from the text"""
        text = re.sub('(?P<url>https?://[^\s]+)', '', text)
        return text

def find_all_hashtags(text):
        """searches the text for hashtags and returns them"""
        searchStr = '\B#\w*[a-zA-Z]+\w*'
        result = re.findall(searchStr, text)
        return result

def nr_of_urls(text):
    #takes the text of a tweet and return the number of urls
    return len(find_all_urls(text))

def avg_url_length(text):
    #returns the average url length
    urls = find_all_urls(text)
    somma=0
    for url in urls:
        somma+=len(url)
    return round(somma/len(urls), 2)

def url_only(text):
    #verify if the text of a tweet is made by urls 
    text=remove_urls(text)
    text=re.sub('[^A-Za-z0-9]+', '', text) 
    if(len(text)==0):
        return True
    return False

def nr_of_hashtag(text):
    return len(find_all_hashtags(text))

def nr_of_popular_hashtag(text):
    pass

def nr_of_punctuation(text):
    #returns the number of punctuation character used in the actual text of a tweet
    punteggiatura = list(string.punctuation) + ['’', '…', '‘', '“', '”']
    somma=0
    for carattere in remove_urls(text):
        if carattere in punteggiatura:
            somma+=1
    return somma

def nr_of_exclamation_marks(text):
    somma=0
    for carattere in remove_urls(text):
        if carattere == '!':
            somma+=1
    return somma

def nr_of_question_marks(text):
    somma=0
    for carattere in remove_urls(text):
        if carattere == '?':
            somma+=1
    return somma

def character_repetitions(text):
    pass

if __name__=="__main__":
    text="@playbingobash Gems are sparkling everywhere! in #BingoBash!!! http://bash.gg/1Y35AQ0"

    print("nr_of_#: ", nr_of_hashtag(text))
    print("nr_of_punctuation: ", nr_of_punctuation(text))
    print("nr of exclamation marks: ", nr_of_exclamation_marks(text))
    print("nr of question marks: ", nr_of_question_marks(text))
    #print("avg_url_length: ", avg_url_length(text))
    #print("url_only: ", url_only(text))
