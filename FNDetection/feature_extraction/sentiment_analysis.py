from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment_score(text):
    sent_analizer=SentimentIntensityAnalyzer()
    return sent_analizer.polarity_scores(text)

text="you are fcking stupid my friend"
print(sentiment_score(text))