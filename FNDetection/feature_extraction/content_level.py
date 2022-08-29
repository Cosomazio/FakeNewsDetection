import re
import string
import emoji
from tweet_level import remove_urls

#to change when tweepy works
def remove_mention(text):
    text = re.sub('(@[^\s]+)','',text)
    return text

def remove_punctuation(text):
    """removes punctuation for the text"""
    for c in string.punctuation:
        text = text.replace(c,'')
    return text

def clearText(text):
    return remove_punctuation(remove_urls(text))

def contains_number(text):
    for word in text:
        if word.isdigit():
            return True
    return False

def contains_quotes(text):
    #due flagghine per giggino
    up=False
    down=False
    for i in range(len(text)//2):
        j=len(text)-1-i
        if "\"" in text[i]: up=True
        if "\"" in text[j]: down=True
    
    return up & down

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
    if(len(text)==0):
        return 0
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
text = """ ciao amico -12  "bla bla bla" mi piace giovanna """
print(no_text(text), text)