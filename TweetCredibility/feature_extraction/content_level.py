import json
import emoji
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from feature_extraction.text_processing import *

from spellchecker import SpellChecker

def contains_number(text):
    """ """
    for word in text:
        if word.isdigit():
            return True
    return False

def contains_quotes(text):
    """ """
    up=False
    down=False
    for i in range(len(text)//2):
        j=len(text)-1-i
        if "\"" in text[i]: up=True
        if "\"" in text[j]: down=True
    
    return up & down

def no_text(text):
    """ """
    text = clearText(text)
    text = text.split()
    if len(text) == 0:
        return True
    else:
        return False

def avg_word_length(text):
    """ """
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
    text = clearText(text)
    text = text.replace(" ",'')
    count =0
    for word in text:
        if word == word.upper():
            count +=1
    return True if count == len(text) else False

def contains_uppercase_text(text):
    """check if the text contain a sequence of chatacter of length five or larger that contain only uppercase letters"""
    text = clearText(text)
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
    clearText(text)
    text = text.replace(" ",'')
    count =0
    for word in text:
        if word == word.upper():
            count +=1
    return count

def ratio_capitalized_words(text):
    """Counts the number of capitalized words and relates them to the word count.
    Words with only capitalized characters are not included in the count for capitalized words."""
    text=clearText(text)
    sum=leng=0
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
    text = clearText(text)
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

    text = clearText(text)
    if len(text) ==0:
        return 0
    return len(tokenization(text))

def nr_of_tokens(text):
    """ returns the number of tokens in the text without counting user mentions and urls"""
    text = remove_mention(remove_urls(text))
    return len(tokenization(text)) #cambiare il tokenizzatore

def num_of_slang_words(text):
    """ """
    count=0
    with open("./feature_extraction/resources/slang_words.json","r") as file:
        data = json.load(file)
    text=tokenization(text) #cambiare con tokenizzazione e no contrazione
    for word in text:
        if word in data:
            count+=1
    return count

def ratio_adjectives(text):
    """ """
    count = 0
    text = clearText(text)

    toktext = tokenization(text)
    toktext = replace_slang(toktext)
    wordslist = [w for w in toktext]

    tagged = pos_tag(wordslist)
    for el in tagged:
        if el[1][0] == 'J':
            count+=1 
    return count/len(wordslist)

def ratio_verbs(text):
    """ """
    count = 0
    text = clearText(text)

    toktext = tokenization(text)
    toktext = replace_slang(toktext)
    wordslist = [w for w in toktext]

    tagged = pos_tag(wordslist)
    for el in tagged:
        if el[1][0] == 'V' or el[1]=="MD":
            count+=1 
    return count/len(wordslist)

def ratio_nouns(text):
    """ """
    count = 0
    text = clearText(text)
    
    toktext = tokenization(text)
    toktext = replace_slang(toktext)
    wordslist = [w for w in toktext]

    tagged = pos_tag(wordslist)
    
    for el in tagged:
        if el[1][0] == 'N':
            count+=1 
    return count/len(wordslist)

def contains_pronouns(text):
    """ """
    text = clearText(text)

    toktext = tokenization(text)
    toktext = replace_slang(toktext)
    wordslist = [w for w in toktext]

    tagged = pos_tag(wordslist)
    
    for el in tagged:
        if el[1][0] == 'P' and el[1] != "PDT":
            return True
    return False

def ratio_stopwords(text):
    """ """
    text = clearText(text)
    stop_words = set(stopwords.words('english'))

    toktext = tokenization(text)
    toktext = replace_slang(toktext)
    
    wordslist = [w for w in toktext if w in stop_words]
    #print(wordslist)
    return len(wordslist)/len(text)

def miSpelling(text):
    """ """
    spell=SpellChecker()
    text = remove_emoji(text)
    text = remove_mention(text)
    text = remove_urls(text)

    toktext = tokenization(text)
    toktext = replace_slang(toktext)

    misspelled= [el for el in spell.unknown(text)]
    return len(misspelled)!=0
    
if __name__ == "__main__":
    print(no_text("This😂😂 is a @prova 😂"))
    text = """ ciao amico -12  "bla bla bla" mi piace giovanna """
    text = "CIA A TUTTg. Sono bello U.S. Miao"

    print(num_of_sentences(text), text)
    
    text="CIAO MY FRI,END,COME TE LA PASSI? IO STO"
    text1=":) This😂😂 is a @prova 😂"

    print(tokenization(text))
    print(tokenization(text1))
    # print(nr_words_token(text))
    # print(nr_words_token(text1))
    # print(nr_of_tokens(text))
    # print(nr_of_tokens(text1))

    # print(num_of_slang_words("ty man it's ok, but it's 2 l8, fu"))
    """print("adjective ",ratio_adjectives("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print("verbs ",ratio_verbs("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print("nouns ",ratio_nouns("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print(ratio_stopwords("hi boy, you're so cute but i can't fuck you it's 2 l8"))
    print(miSpelling("hi boy, you're so cute but i can't fck you it's 2 l8"))
    """
    #print(remove_emoji(":-<3, :-):("))
    #print(avg_word_length("hi boy, you're, so cute but i can't fuck you it's 2 l8"))
