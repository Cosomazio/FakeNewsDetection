import re
import string
import emoji
from tweet_level import remove_urls
from nltk.tokenize import sent_tokenize, word_tokenize


#to change when tweepy works
def remove_mention(text):
    text = re.sub('(@[^\s]+)','',text)
    return text

def remove_punctuation(text):
    """removes punctuation for the text"""
    for c in string.punctuation:
        text = text.replace(c,'')
    return text

def remove_emoji(text):
    for el in text:
        if emoji.is_emoji(el):
            text = text.replace(el,'')
    return text

def clearText(text):
    text = remove_emoji(text)
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
    """return the length of the text according to the Twitter character counting"""
    count = 0
    text = remove_mention(text)
    for word in text:
        if emoji.is_emoji(word):
            count +=2
        else:
            count +=1
    return count

def is_all_uppercase(text):
    """check if the text are all in uppercase"""
    text = text.replace(" ",'')
    count =0
    for word in text:
        if word == word.upper():
            count +=1
    return True if count == len(text) else False

def contains_uppercase_text(text):
    """check if the text contain a sequence of chatacter of length five or larger that contain only uppercase letters"""
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)
    text = text.replace(" ",'')
    cont=False
    count =0
    for word in text:
        if word == word.upper():
            count +=1
            if count >= 5 : cont=True
        else:
            count = 0
    return cont

def count_upper_letter(text):
    """Counts the number of uppercase letter"""
    text = text.replace(" ",'')
    count =0
    for word in text:
        if word == word.upper():
            count +=1
    return count

def ratio_capitalized_words(text):
    """Counts the number of capitalized words and relates them to the word count.
    Words with only capitalized characters are not included in the count for capitalized words."""
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)
    sum=leng=0
    #text = text.replace(" ",'')
    text = text.split()
    for word in text:
        leng+=len(word)
        if word == word.upper():
            continue
        else:
            sum += (count_upper_letter(word))
    
    return round(sum/leng,2)

def ratio_all_capitalized_words(text):
    """Ratio of words that contain only capitalized letters to the total number of words."""
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)
    sum=leng=0
    text=text.split()

    for word in text:
        leng+=len(word)
        if word != word.upper():
            continue
        else:
            sum += (count_upper_letter(word))
    
    return round(sum/leng,2)

def num_of_sentences(text):
    """Counts the number of sentences."""
    tok=sent_tokenize(text)
    return len(tok)

def nr_words_token(text):
    """ returns the numbner of tokens that are actual words without counting user mentions, emoji and urls"""
    text= remove_mention(text)
    text = clearText(text)
    if len(text) ==0:
        return []
    return len(word_tokenize(text))

def nr_of_tokens(text):
    """ returns the number of tokens in the text without counting user mentions and urls"""
    text = remove_mention(remove_urls(text))
    return len(word_tokenize(text))


if __name__ == "__main__":
    print(no_text("This😂😂 is a @prova 😂"))
    text = """ ciao amico -12  "bla bla bla" mi piace giovanna """
    text = "CIA A TUTTg. Sono bello U.S. Miao"

    print(num_of_sentences(text), text)

    text="CIAO MY FRIEND, COME TE LA PASSI? IO STO"
    text1="This😂😂 is a @prova 😂"

    print(nr_words_token(text))
    print(nr_words_token(text1))
    print(nr_of_tokens(text))
    print(nr_of_tokens(text1))
