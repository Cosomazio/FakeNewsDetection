import tweepy

""" autenticazione quando viene abilitato l'accesso elevated"""
def api_v1_connection():
    consumer_key = ""
    consumer_secret = ""

    access_token = ""
    access_token_secret= ""
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)

    return api

"""accesso per api v2 attraverso client"""
def api_v2_connection():
    bearer_token = ""
    consumer_key = ""
    consumer_secret = ""

    access_token = ""
    access_token_secret= ""
    client = tweepy.Client(bearer_token=bearer_token,consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

    return client

