import json
import re
import string
import emoji
from tweet_level import remove_urls
from nltk.tokenize import sent_tokenize, word_tokenize,regexp_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from spellchecker import SpellChecker

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
#to change when tweepy works
def remove_mention(text):
    text = re.sub('(@[^\s]+)','',text)
    return text

def remove_slang(text):
    with open("FNDetection/feature_extraction/resources/slang_words.json","r") as file:
        data = json.load(file)

    text = tokenization_no_contr(text)

    for word in text:
        if word in data:
            text[text.index(word)]=data[word]
    return text

def remove_punctuation(text):
    """removes punctuation for the text"""
    punteggiatura = list(string.punctuation) + ['’', '…', '‘', '“', '”']
    for c in punteggiatura:
        text = text.replace(c,' ')
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
    return len(tokenization_no_contr(text))

def nr_of_tokens(text):
    """ returns the number of tokens in the text without counting user mentions and urls"""
    text = remove_mention(remove_urls(text))
    return len(word_tokenize(text))

def num_of_slang_words(text):
    count=0
    with open("FNDetection/feature_extraction/resources/slang_words.json","r") as file:
        data = json.load(file)
    text=tokenization_no_contr(text)
    for word in text:
        if word in data:
            count+=1
    return count

def tokenization_no_contr(text):
    st=""
    text = text.split()
    for el in text:
        el = replace_contractions_text(el)
        st+=el+" "
    text= regexp_tokenize(st,"[\w’]+")
    return text

def ratio_adjectives(text):
    count = 0
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)

    text = remove_slang(text)
    wordslist = [w for w in text]

    tagged = pos_tag(wordslist)
    for el in tagged:
        if el[1][0] == 'J':
            count+=1 
    return count/len(wordslist)

def ratio_verbs(text):
    count = 0
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)

    text = remove_slang(text)

    wordslist = [w for w in text]

    tagged = pos_tag(wordslist)
    for el in tagged:
        if el[1][0] == 'V' or el[1]=="MD":
            count+=1 
    return count/len(wordslist)

def ratio_nouns(text):
    count = 0
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)

    text = remove_slang(text)

    wordslist = [w for w in text]

    tagged = pos_tag(wordslist)
    
    for el in tagged:
        if el[1][0] == 'N':
            count+=1 
    return count/len(wordslist)

def contains_pronouns(text):
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)

    text = remove_slang(text)

    wordslist = [w for w in text]

    tagged = pos_tag(wordslist)
    
    for el in tagged:
        if el[1][0] == 'P' and el[1] != "PDT":
            return True
    return False

def ratio_stopwords(text):
    text = remove_mention(text)
    text = remove_emoji(text)
    text = remove_urls(text)
    stop_words = set(stopwords.words('english'))

    text = remove_slang(text)
    
    wordslist = [w for w in text if w in stop_words]
    print(wordslist)
    return len(wordslist)/len(text)

def miSpelling(text):
    spell=SpellChecker()
    text = remove_emoji(text)
    text = remove_mention(text)
    text = remove_slang(text)

    misspelled= [el for el in spell.unknown(text)]
    return len(misspelled)!=0
    
if __name__ == "__main__":
    print(no_text("This😂😂 is a @prova 😂"))
    text = """ ciao amico -12  "bla bla bla" mi piace giovanna """
    text = "CIA A TUTTg. Sono bello U.S. Miao"

    print(num_of_sentences(text), text)
    
    text="CIAO MY FRIEND, COME TE LA PASSI? IO STO"
    text1="This😂😂 is a @prova 😂"

    # print(nr_words_token(text))
    # print(nr_words_token(text1))
    # print(nr_of_tokens(text))
    # print(nr_of_tokens(text1))

    # print(num_of_slang_words("ty man it's ok, but it's 2 l8, fu"))
    print("adjective ",ratio_adjectives("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print("verbs ",ratio_verbs("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print("nouns ",ratio_nouns("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print(ratio_stopwords("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print(miSpelling("hi boy, you're so cute but i can't fck you it's 2 l8"))
    #print(avg_word_length("hi boy, you're, so cute but i can't fuck you it's 2 l8"))
