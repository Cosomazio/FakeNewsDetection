from feature_extraction.twitter_api import *
from feature_extraction.tweet_level import *
import time
import datetime
from datetime import date

def desc_contains_hashtags(user):
    result = nr_of_hashtag(get_description(user))
    if result:
        return True
    return False

def desc_contains_user_mention(user, v2_connection):
    desc = get_description(user)
    result = num_of_usermention(desc)
    if result != 0:
        return True
    return False

def desc_contains_url(user):
    result = nr_of_urls(get_description(user))
    if result != 0:
        return True
    return False

def desc_length(user):
    return len(get_description(user))

def url_lenght(user):
    if hasattr(user, "url"):
        if user.url is not None:
            return len(user.url)
        else: return 0
    else: return 0

def friends_per_followers(user):
    friend=friends_count(user)
    follow=followers_count(user)
    return round(friend/follow,5) if follow != 0 else 0

def is_following_more_than_100(user):
    return True if followers_count(user) >= 100 else False

def created_days_ago(user):
    date_format= "%Y-%m-%d"
    date_today=time.strptime(str(date.today()),date_format)
    date_today = datetime.datetime.fromtimestamp(time.mktime(date_today)) 
    date_created=time.strptime(str(user.created_at).split()[0],date_format)
    date_created = datetime.datetime.fromtimestamp(time.mktime(date_created))
    return(date_today-date_created).days
