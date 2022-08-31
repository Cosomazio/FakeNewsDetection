from content_level import remove_mention, remove_urls, remove_slang, pos_tag, lemmatize
from emoji import is_emoji
from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    text = remove_mention(remove_urls(text))
    pos_score = analyzer.polarity_scores(text)['pos']
    neg_score = analyzer.polarity_scores(text)['neg']
    #devo tokenizzare le parole e fare len(stringa di parole)
    parole=text.split()
    score = (((pos_score - neg_score)/len(parole))+1)/2
    return score

text="<3" 
anal = SentimentIntensityAnalyzer()
print(sentiment_score(text))