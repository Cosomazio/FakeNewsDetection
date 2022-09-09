from twitter_api import *
from tweet_level import *
import time
import datetime
from datetime import date

def get_description(user_id):
    client = api_v2_connection()
    user = client.get_user(id=user_id,user_fields=["description"])
    return user.data.description

def has_desc(user_id):
    if len(get_description(user_id)) != 0:
        return True
    return False

def desc_contains_hashtags(user_id):
    result = nr_of_hashtag(get_description(user_id))
    if result:
        return True
    return False

def desc_contains_user_mention(user_id):
    result = num_of_usermention(get_description(user_id))
    if result != 0:
        return True
    return False

def desc_contains_url(user_id):
    result = nr_of_urls(get_description(user_id))
    if result != 0:
        return True
    return False

def desc_length(user_id):
    return len(get_description(user_id))

def url_lenght(user_id):
    client = api_v2_connection()
    user = client.get_user(id=user_id,user_fields=["url"])
    return len(user.data.url)

def friends_per_followers(user_id):
    friend=friends_count(user_id,api_v2_connection())
    follow=followers_count(user_id,api_v2_connection())
    return round(friend/follow,5) if follow != 0 else 0

def is_following_more_than_100(user_id):
    return True if followers_count(user_id,api_v2_connection()) >= 100 else False

def created_days_ago(user_id):
    client = api_v2_connection()
    date_format= "%Y-%m-%d"
    user = client.get_user(id=user_id,user_fields=["created_at"])
    date_today=time.strptime(str(date.today()),date_format)
    date_today = datetime.datetime.fromtimestamp(time.mktime(date_today))
    date_created=time.strptime(str(user.data.created_at).split()[0],date_format)
    date_created = datetime.datetime.fromtimestamp(time.mktime(date_created))
    return(date_today-date_created).days
   
if __name__ == "__main__":
    #id=1518948046809219076
    #id=38001497
    id=32871086

    print("Has description:",has_desc(id))
    print("Description contain hashtags:",desc_contains_hashtags(id))
    print("Description contain url:",desc_contains_url(id))
    print("Description contain user mention:",desc_contains_user_mention(id))
    print("Description lenght:",desc_length(id))
    print("User URL lenght:",url_lenght(id))
    print("Friend per followers:",friends_per_followers(id))
    print("Following more than 100:",is_following_more_than_100(id))
    print("created day ago:",created_days_ago(id))