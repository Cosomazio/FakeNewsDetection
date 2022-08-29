import re
from curses.ascii import isdigit
import string
import emoji

def remove_url(text):
    """removes urls from the text"""
    text = re.sub('(?P<url>https?://[^\s]+)', '', text)
    return text

def remove_mention(text):
    text = re.sub('(@[^\s]+)','',text)
    return text

def remove_punctuation(text):
    """removes punctuation for the text"""
    for c in string.punctuation:
        text = text.replace(c,'')
    return text

def clearText(text):
    return remove_punctuation(remove_url(text))

def contains_number(text):
    for word in text:
        if word.isdigit():
            return True
    return False

def contains_quotes(text):
    text = text.split()
    for word in text:
        if "\"" in word:
            return True
    return False

def no_text(text):
    text = clearText(text)
    text = text.split()
    if len(text) == 0:
        return True
    else:
        return False

def avg_word_length(text):
    sum = 0
    text = clearText(text)
    text = text.split()
    for word in text:
        current_sum=0
        current_sum+=len(word)
        sum += current_sum
    return sum/len(text)

def text_length(text):
    count = 0
    text = remove_mention(text)
    for word in text:
        if emoji.is_emoji(word):
            count +=2
        else:
            count +=1
    return count

print(text_length("This is a @prova"))