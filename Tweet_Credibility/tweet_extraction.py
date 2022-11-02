from sys import argv
from feature_extraction.twitter_api import api_v1_connection, get_tweet_status
import sys
import json
import re


class Tweet:
    _text=""
    _user_name=""
    _user_image=""
    _medias=None
    
    def __init__(self, text, username, userimage, medias):
        self._text = text
        self._user_name=username
        self._user_image = userimage
        self._medias=medias

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False)

if __name__ == "__main__":
    id = argv[1]
    v1_conn = api_v1_connection()
    try:
        status = get_tweet_status(id, v1_conn)
        #print(status)
        user = status.user._json['name']
        userimage = status.user._json['profile_image_url_https']
        if  "extended_entities" in status._json:
            medias = [el['media_url_https'] for el in status._json['extended_entities']['media'][:]]
        elif "media" in status._json['entities']:
            medias = [el['media_url_https'] for el in status.entities['media'][:]]
        else:
            medias =[]
        #print(medias)
        text=re.sub(r' https://t.co/\w{10}', '', status.text)
        print(Tweet(text, user, userimage, medias).toJSON())
    except:
        sys.exit(-1)
    