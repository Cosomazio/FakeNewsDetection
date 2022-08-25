from socialCredibility import socialCredibility
from userCredibility import userCredibility
from textCredibility import textCredibility

def credibility(tweetPath, social_weight=0.33, user_weight=0.33, text_weight=0.34):
    return textCredibility(tweetPath)*text_weight+userCredibility(tweetPath)*user_weight+socialCredibility(tweetPath)*social_weight
