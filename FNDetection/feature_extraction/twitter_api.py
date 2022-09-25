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

""" return the author id of a tweet, given the tweet id"""
def get_user_id(tweet_id, v2_connection):
    tweet = v2_connection.get_tweet(tweet_id, expansions=['author_id'])
    return tweet.data.author_id

def get_tweet_text(tweet_id, v1_connection):
    
    tweet = v1_connection.get_status(tweet_id)
    return tweet.text

def followers_count(user_id, v2_connection):
    user =v2_connection.get_user(id=user_id, user_fields=["public_metrics"])
    return user.data.public_metrics['followers_count']

def friends_count(user_id, v2_connection):
    user =v2_connection.get_user(id=user_id, user_fields=["public_metrics"])
    return user.data.public_metrics['following_count']

def statuses_count(user_id, v2_connection):
    user = v2_connection.get_user(id=user_id, user_fields=['public_metrics'])
    return user.data.public_metrics['tweet_count']

def verified(user_id, v2_connection):
    user = v2_connection.get_user(id=user_id, user_fields=["verified"])
    return user.data.verified

def default_profile(user_id, v1_connection):
    user = v1_connection.get_user(user_id=user_id)
    return user.default_profile

def profile_background_tile(user_id, v1_connection):
    user = v1_connection.get_user(user_id=user_id)
    return user.profile_background_tile

def profile_use_background_image(user_id,v1_connection):
    user = v1_connection.get_user(user_id=user_id)
    return user.profile_use_background_image

def favorite_count(tweet_id, v1_connection):
    status = v1_connection.get_status(tweet_id)
    return status.favorite_count

def retweeted_count(tweet_id, v1_connection):
    status = v1_connection.get_status(tweet_id)
    return status.retweet_count

def truncated(tweet_id, v1_connection):
    status = v1_connection.get_status(tweet_id)
    return status.truncated

def possibly_sensitive(tweet_id, v1_connection):
    status = v1_connection.get_status(tweet_id)
    return status.possibly_sensitive



if __name__ == "__main__":
    id = 1344776928583159817
    connection = api_v2_connection()
    uid=get_user_id(id, connection)
    
    print(connection.get_user(id=uid, user_fields=['entities']).data.entities)

    v1_connection = api_v1_connection()
    print(possibly_sensitive(id, v1_connection))
    print(retweeted_count(id, v1_connection))
    print(favorite_count(id, v1_connection))
    print(truncated(id, v1_connection))

    print(default_profile(uid, v1_connection))
    print(profile_background_tile(uid, v1_connection))
    print(profile_use_background_image(uid, v1_connection))

    #print(get_user_id(id, connection))
    #print(friends_count(get_user_id(id, connection), connection))
    #print(statuses_count(get_user_id(id, connection), connection))
    #print(verified(get_user_id(id, connection), connection))