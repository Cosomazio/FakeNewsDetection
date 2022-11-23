from nltk import WordNetLemmatizer
import re
import json
import string
import emoji
from nltk.tokenize import regexp_tokenize

def lemmatize(token, pos_tag):
    """utility that convert lemmatization labels into others comprehensible to the standard lemmatizer and returns
    the lemmatized versione of that token"""
    if pos_tag == 'J':
        pos_tag='a'
    elif pos_tag == 'N':
        pos_tag='n'
    elif pos_tag == 'R':
        pos_tag='r'
    elif pos_tag == 'V':
        pos_tag='v'
    else:
        return token

    lemmatizer= WordNetLemmatizer()
    return lemmatizer.lemmatize(token, pos_tag)

#to change when tweepy works
def remove_mention(text):
    """ removes those user mentions present in the given text"""
    text = re.sub('(@[^\s]+)','',text)
    return text

def replace_slang(tokenized_text):
    """replaces slang words in the given tokenized text"""
    with open("./feature_extraction/resources/slang_words.json","r") as file:
        data = json.load(file)
    
    for word in tokenized_text:
        if word in data:
            tokenized_text[tokenized_text.index(word)]=data[word]
    return tokenized_text

def remove_punctuation(text):
    """removes punctuation for the text"""
    punteggiatura = list(string.punctuation) + ['’', '…', '‘', '“', '”']
    for c in punteggiatura:
        text = text.replace(c,'')
    return text

def remove_emoji(text, path=None):
    """ removes ascii emoji and unicode emoji from a given text"""
    for el in text:
        if emoji.is_emoji(el):
            text = text.replace(el,'')
    if(path is None):
        with open("./feature_extraction/resources/ascii_emojis.json", 'r') as file:
            emojis=json.load(file)
    else:
        with open(path, 'r') as file:
            emojis=json.load(file)
    
    for el in emojis:
        if el in text:
            text = text.replace(el, '') 

    return text

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

def clearText(text):
    """ removes emojis, user mentions, urls and punctuation from the given text"""
    text = remove_emoji(text)
    text = remove_mention(text)
    text = remove_urls(text) 
    return remove_punctuation(text)

def tokenization(text):
    """tokenization of the given text"""
    regexp=r"[\w']+|["
    for el in emoji.unicode_codes.data_dict.EMOJI_DATA:
        regexp+=el
    regexp+="]|[^a-zA-Z]{1,3}"

    text = regexp_tokenize(text, regexp)
    text = [el for el in text if el !=' ']
    return text

def replace_contractions(text):
    """replaves contractions in the given text with the its extended english version"""
    st=""
    text = text.split()
    for el in text:
        el = replace_contractions_text(el)
        st+=el+" "
    
    return st

def replace_contractions_text(token):
        """short form replacement from http://speakspeak.com/resources/english-grammar-rules/various-grammar-rules/short-forms-contractions
        Some are ambiguous like 'd= had or would
        DONE BY TweetTokenizer!!"""

        token = token.replace("can't", "can not")
        token = token.replace("Can't", "Can not")
        token = token.replace("n't", " not")
        token = token.replace("I'm", "I am")
        token = token.replace("He's", "He is")
        token = token.replace("he's", "he is")
        token = token.replace("She's", "She is")
        token = token.replace("she's", "she is")
        token = token.replace("It's", "It is")
        token = token.replace("it's", "it is")
        token = token.replace("You're", "You are")
        token = token.replace("you're", "you are")
        token = token.replace("We're", "We are")
        token = token.replace("we're", "we are")
        token = token.replace("They're", "They are")
        token = token.replace("they're", "they are")
        token = token.replace("You've", "You have")
        token = token.replace("you've", "you have")
        token = token.replace("I've", "I have")
        token = token.replace("We've", "We have")
        token = token.replace("we've", "we have")
        token = token.replace("They've", "They have")
        token = token.replace("they've", "they have")
        token = token.replace("Let's", "Let us")
        token = token.replace("let's", "let us")
        token = token.replace("Who's", "Who is")
        token = token.replace("who's", "who is")
        token = token.replace("Who'd", "Who would")
        token = token.replace("who'd", "who would")
        token = token.replace("What's", "What is")
        token = token.replace("what's", "what is")
        token = token.replace("How's", "How is")
        token = token.replace("how's", "how is")
        token = token.replace("When's", "When is")
        token = token.replace("when's", "when is")
        # includes there's, where's
        token = token.replace("here's", "here is")
        token = token.replace("Here's", "Here is")
        token = token.replace("There's", "There is")
        token = token.replace("there'd", "there would")
        token = token.replace("There'd", "There would")
        token = token.replace("that's", "that is")
        token = token.replace("That's", "That is")
        # 'll always resolves to ' will
        token = token.replace("'ll", " will")

        # ambiguous would and had
        token = token.replace("I'd", "I would")
        token = token.replace("He'd", "He would")
        token = token.replace("he'd", "he would")
        token = token.replace("She'd", "She would")
        token = token.replace("she'd", "she would")
        token = token.replace("It'd", "It would")
        token = token.replace("it'd", "it would")
        token = token.replace("You'd", "You would")
        token = token.replace("you'd", "you would")
        token = token.replace("We'd", "We would")
        token = token.replace("we'd", "we would")
        token = token.replace("They'd", "They would")
        token = token.replace("they'd", "they would")

        return token