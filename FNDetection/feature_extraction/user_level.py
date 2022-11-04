from feature_extraction.twitter_api import *
from feature_extraction.tweet_level import *
import time
import datetime
from datetime import date

""" verifies if the user description contains hashtags"""
def desc_contains_hashtags(user):
    result = nr_of_hashtag(get_description(user))
    if result>0:
        return True
    return False

""" verifies if the user description contains user mentions"""
def desc_contains_user_mention(user, v2_connection):
    desc = get_description(user)
    result = num_of_usermention(desc)
    if result != 0:
        return True
    return False

""" verifies if the user description contains urls"""
def desc_contains_url(user):
    result = nr_of_urls(get_description(user))
    if result != 0:
        return True
    return False

""" returns the length of the user description """
def desc_length(user):
    return len(get_description(user))

""" return the length of the url describing the given user"""
def url_lenght(user):
    if hasattr(user, "url"):
        if user.url is not None:
            return len(user.url)
        else: return 0
    else: return 0

""" computes the ratio between followers and friends for the given user"""
def friends_per_followers(user):
    friend=friends_count(user)
    follow=followers_count(user)
    return round(friend/follow,5) if follow != 0 else 0

""" verifies if the user follows more than 100 accounts"""
def is_following_more_than_100(user):
    return True if followers_count(user) >= 100 else False

""" computes the number of days since this account was created"""
def created_days_ago(user):
    date_format= "%Y-%m-%d"
    date_today=time.strptime(str(date.today()),date_format)
    date_today = datetime.datetime.fromtimestamp(time.mktime(date_today)) 
    date_created=time.strptime(str(user.created_at).split()[0],date_format)
    date_created = datetime.datetime.fromtimestamp(time.mktime(date_created))
    return(date_today-date_created).days

   
if __name__ == "__main__":
    #id=1518948046809219076
    #id=38001497
    id=32871086
    v2_connection = api_v2_connection()
    v1_connection = api_v1_connection()
    user = v1_connection.get_user(user_id=id)
    #print("Has description:",has_desc(id))
    #print(get_description(id, v2_connection))
    print("created day ago:",created_days_ago(user))
    
    """print("Description contain hashtags:",desc_contains_hashtags(id))
    print("Description contain url:",desc_contains_url(id))
    print("Description contain user mention:",desc_contains_user_mention(id))
    print("Description lenght:",desc_length(id))
    print("User URL lenght:",url_lenght(id))
    print("Friend per followers:",friends_per_followers(id))
    print("Following more than 100:",is_following_more_than_100(id))
    print("created day ago:",created_days_ago(id))"""