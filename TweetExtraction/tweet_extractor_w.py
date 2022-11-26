import tweepy
import json
from tqdm import tqdm

def api_v2_connection():
    bearer_token = "" 
    consumer_key = "" 
    consumer_secret = ""

    access_token = ""
    access_token_secret= ""
    client = tweepy.Client(bearer_token=bearer_token,consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret,wait_on_rate_limit=True)
    
    return client

def api_v1_connection():
    bearer_token = "" 
    consumer_key = "" 
    consumer_secret = ""

    access_token = ""
    access_token_secret= ""
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return api

def get_tweet_status(twid, v1_connection):
    status = v1_connection.get_status(twid, tweet_mode="extended")
    return status

if __name__ == "__main__":
    query=[]
    #query.append("#covid lang:en")
    #query.append("#war lang:en")
    #query.append("#election lang:en")
    query.append("#ukraine lang:en")
    query.append("#putin lang:en")
    query.append("#earthquake lang:en")
    
    apis = api_v1_connection()
    client =api_v2_connection()
    for q in query:
        with open("listid.txt","w") as file:
            file.write("")
        print("query:", q)
        tweets = tweepy.Paginator(client.search_recent_tweets, query=q, max_results=100).flatten(limit=3000)  
        lid=[el.id for el in tweets]
        with open("listid.txt","a") as file:
            for el in tqdm(lid):
                file.write(str(el)+"\n")
        for id in lid:
            try:
                print("CURRENT ID: ",id)
                status = get_tweet_status(id,apis)
                json_object = json.dumps(status._json,indent=5)
                with open("5Nov12Nov.json", "a") as outfile:
                    outfile.write(json_object)
            except:
                print("ID NOT FOUND: ",id)
                continue

