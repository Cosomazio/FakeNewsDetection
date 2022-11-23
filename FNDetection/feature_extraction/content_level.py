import emoji
from feature_extraction.text_processing import *

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


def nr_words_token(text):
    """ returns the numbner of tokens that are actual words without counting user mentions, emoji and urls"""

    text = clearText(text)
    if len(text) ==0:
        return 0
    return len(tokenization(text))

    
if __name__ == "__main__":
    text = """ ciao amico -12  "bla bla bla" mi piace giovanna """
    text = "CIA A TUTTg. Sono bello U.S. Miao"

    
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
