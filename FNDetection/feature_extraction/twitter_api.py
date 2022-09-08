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
    
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAPhmgwEAAAAAedGk1%2B4IV00eDILldAy7Wg5981M%3DaZfqhLUymBDG03ocQzAQex2qXV3eWW8thMsSKoxTNNNx4TESDu"
    consumer_key = "Jiljo6C1lQHORyBSvx0f7rocP"
    consumer_secret = "VNiq5PdogsmWpqDlm81s3qqxDbQBmFYkSS8OkabN1zb2IHGtp9"

    access_token = "1567779884130344960-gf5tbhFi8RPBzrZwSkatbS0vzrC9Vy"
    access_token_secret= "k3c4kR8XnZdMIEpP4zSOZnKdzP8XCbxVjXqLIoBBfAmxc"
    client = tweepy.Client(bearer_token=bearer_token,consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    
    return client

""" return the author id of a tweet, given the tweet id"""
def get_user_id(tweet_id):
    client = api_v2_connection()

    tweet = client.get_tweet(tweet_id, expansions=['author_id'])
    print(tweet)
    return tweet.data.author_id

if __name__ == "__main__":
    id = 1344776928583159817
    print(get_user_id(id))