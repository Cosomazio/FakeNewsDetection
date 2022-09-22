import sys
sys.path.insert(1, '../FakeNewsDetection/FNDetection/feature_extraction')

from twitter_api import api_v2_connection

i=0
api = api_v2_connection()
q=""
res= api.search_recent_tweets(query= q, max_results=10)
for el in res.data:
    print(el.id)
    

