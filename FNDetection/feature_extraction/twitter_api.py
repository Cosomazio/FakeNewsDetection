import tweepy

bearer_token = ""
consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret= ""

""" autenticazione quando viene abilitato l'accesso elevated"""
#auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
#auth.set_access_token(access_token,access_token_secret)
#api = tweepy.API(auth)
#query = "covid lang:en"


"""accesso per api v2 attraverso client """
client = tweepy.Client(bearer_token=bearer_token,consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
#print(client.get_tweet(id="552791196247269378"))

ids=[552791196247269378,529687410611728384]
tweets= client.get_tweets(ids=ids, expansions=['author_id'])
print(tweets.data)
#users = client.get_users(tweets.data['id'])
#user_fields=["verified,location,public_metrics,profile_image_url,default_profile"]
for t in tweets.data:
    print("AAA",t.author_id)
    print("user: ", client.get_user(id=t.data.author_id,user_fields=["verified,location,public_metrics,profile_image_url"]).data.public_metrics)
#file = "/Users/cosimocorbisiero/Downloads/train.csv"

# #b=tweepy.Cursor(api.search_tweets(q="covid")).items(10)
# for a in tweets.data:
#     print(a.text)