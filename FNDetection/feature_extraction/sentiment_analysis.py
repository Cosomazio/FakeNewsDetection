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
    """if(len(text)==0):
        return 0.5
    
    token_text=remove_slang(text)
    
    pos_text = pos_tag(token_text)
    
    accepted_tags = ['J', 'V', 'N', 'R']
    score=0
    for p in pos_text:
        if p[1][0] in accepted_tags:
            word = lemmatize(p[0], p[1][0])

            pos_score=analyzer.polarity_scores(word)['pos']
            neg_score = analyzer.polarity_scores(word)['neg']
            print(pos_score, neg_score, word)
            word_score = pos_score-neg_score
            score+=word_score
    print(score)
    score = ((score/len(pos_text)+1)/2)"""
    return score

text="<3" 
anal = SentimentIntensityAnalyzer()
print(sentiment_score(text))
print(anal.polarity_scores(text))