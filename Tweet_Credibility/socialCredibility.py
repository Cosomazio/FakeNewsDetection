
from feature_extraction.twitter_api import *
MAX_FOLLOWERS = 132500000  #max number of follower on Twitter (Barak Obama)

def socialCredibility(tweet_id):
    
    # user_following = data["user"]["following"] #this is the following of the user
    # user_followers= data["user"]["followers_count"] #this is the followers of the user
    user = get_utente(tweet_id,api_v2_connection(),api_v1_connection())
    if user == None:
        return None
    user_following = friends_count(user)
    user_followers = followers_count(user)

    if user_following == None or user_followers==False:
        user_following = int(0)
    
    #this is the calculation for the follower impact
    follower_impact=(min(user_followers,MAX_FOLLOWERS)/MAX_FOLLOWERS)*50 
    # this is the calculation of proportion between follower and following 
    ff_proportion = (user_followers/(user_followers+user_following))*50

    social_credibility= follower_impact+ff_proportion
    return social_credibility


