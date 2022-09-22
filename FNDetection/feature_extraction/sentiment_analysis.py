from feature_extraction.text_processing import tokenization, remove_urls, remove_mention, replace_slang, lemmatize
from nltk import pos_tag
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def word_score(word):
    analyzer = SentimentIntensityAnalyzer()
    pos_score = analyzer.polarity_scores(word)['pos']
    neg_score = analyzer.polarity_scores(word)['neg']
    return ((pos_score-neg_score)+1)/2

def sentiment_score(text):
    text = remove_mention(remove_urls(text))
    if(len(text)==0):
        return 0.5
    token_text = tokenization(text)
    token_text = replace_slang(token_text)
    wordslist = [w.split()[-1] for w in token_text if len(w.split())>0]

    tagged = pos_tag(wordslist)
    score=0
    for word, tag in tagged:
        lemma_word = lemmatize(word, tag[0])
        
        score+=word_score(lemma_word)
    
    score = (score/len(wordslist))
    return score

def nr_pos_sentiment_words(text):
    text = remove_mention(remove_urls(text))
    if(len(text)==0):
        return 0.5
    token_text = tokenization(text)
    token_text = replace_slang(token_text)
    print(token_text)
    wordslist = [w.split()[-1] for w in token_text if len(w.split())>0]

    tagged = pos_tag(wordslist)
    count=0
    for word, tag in tagged:
        lemma_word = lemmatize(word, tag[0])

        if word_score(lemma_word) >0.5:
            count +=1

    return count

def nr_neg_sentiment_words(text):
    text = remove_mention(remove_urls(text))
    if(len(text)==0):
        return 0.5
    token_text = tokenization(text)
    token_text = replace_slang(token_text)
    wordslist = [w.split()[-1] for w in token_text if len(w.split())>0]

    tagged = pos_tag(wordslist)
    count=0
    for word, tag in tagged:
        lemma_word = lemmatize(word, tag[0])

        if word_score(lemma_word) < 0.5:
            count +=1

    return count


if __name__ == "__main__":
    text="this text :) is a try" 
    anal = SentimentIntensityAnalyzer()
    print(sentiment_score(text))
    print(nr_pos_sentiment_words(text))
    print(nr_neg_sentiment_words(text))