import tweepy

""" autenticazione quando viene abilitato l'accesso elevated"""
def api_v1_connection():
    consumer_key = "" 
    consumer_secret = ""

    access_token = ""
    access_token_secret= ""
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api

"""accesso per api v2 attraverso client"""
def api_v2_connection():
    bearer_token = ""
    consumer_key = "" 
    consumer_secret = ""

    access_token = ""
    access_token_secret= ""
    client = tweepy.Client(bearer_token=bearer_token,consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, wait_on_rate_limit=True)
    
    return client

""" return the author of a tweet, given the tweet id"""
def get_utente(twid, v2_connection, v1_connection):
    tweet = v2_connection.get_tweet(twid, expansions=['author_id'])
    uid = tweet.data.author_id if tweet.data !=None else None
    return v1_connection.get_user(user_id=uid) if uid !=None else None

""" gets the description of the given user """
def get_description(user):
    if hasattr(user, "description"):
        return user.description
    else: return ""

""" return the status representation of the tweet defined by the given id"""
def get_tweet_status(twid, v1_connection):
    status = v1_connection.get_status(twid, tweet_mode="extended")
    return status

""" return the text from the given tweet status"""
def get_tweet_text(tweet):
    if hasattr(tweet, "full_text"):
        return tweet.full_text
    elif hasattr(tweet, "text"):
        return tweet.text
    else:
        return "" 

""" returns the number of follower of the given user"""
def followers_count(user):
    if hasattr(user, "followers_count"):
        return user.followers_count
    else: return 0

""" returns the number of friends of the given user"""
def friends_count(user):
    if hasattr(user, "friends_count"):
        return user.friends_count
    else: return 0

"""returns the number of statuses posted by the given user"""
def statuses_count(user):
    if hasattr(user, "statuses_count"):
        return user.statuses_count
    else: return 0

""" verifies if the given user is verified"""
def verified(user):
    if hasattr(user, "verified"):
        return user.verified
    else: return False

""" verifies if the given user has default profile"""
def default_profile(user):
    if hasattr(user, "default_profile"):
        return user.default_profile
    else: return False

""" verifies if the given user has changed their background image"""
def profile_use_background_image(user):
    if hasattr(user, "profile_use_background_image"):
        return user.profile_use_background_image
    else: return False


if __name__ == "__main__":
    id = 1344776928583159817
    connection = api_v2_connection()
    v1_connection = api_v1_connection()

    user=get_utente(id, connection, v1_connection)
    tweet_status = get_tweet_status(id, v1_connection)
    
    #print(connection.get_user(id=uid, user_fields=['entities']).data.entities)
    
    """print(possibly_sensitive(tweet_status))
    print(retweeted_count(tweet_status))
    print(favorite_count(tweet_status))
    print(truncated(tweet_status))

    print(default_profile(user))
    print(profile_background_tile(user))
    print(profile_use_background_image(user))

    #print(get_user_id(id, connection))
    print(followers_count(user))
    print(friends_count(user))
    print(statuses_count(user))
    print(verified(user))

    print("description", get_description(user))"""