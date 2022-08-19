import json
from datetime import date

SOCIALPLATFORMCREATED = 2006  #Year of creation of Twitter
MAX_FOLLOWERS = 132500000  #max number of follower on Twitter (Barak Obama)

def userCredibility(data):
    
    user=data["user"]
    
    verified_weight=50 if user["verified"] else 0 #this is for see if the user is verfied

    creation_data=data["created_at"].split()
    account_age= date.today().year- int(creation_data[len(creation_data)-1]) #this is the calculation for the age of the profile --> currentYear - YearJoined
    max_account_age= date.today().year - SOCIALPLATFORMCREATED #this is the calculation for the max account age for one profile in Twitter --> currentYear - YearSocialPlatformCreated
    creation_weight=(account_age/max_account_age)* 50 

    # print("Verified weight [0-50]:",verified_weight,user["verified"])
    # print("Creation weight [0-50]:",creation_weight)

    user_credibility= verified_weight + creation_weight
    return user_credibility


def socialCredibility(data):

    user_following = data["user"]["following"] #this is the following of the user
    user_followers= data["user"]["followers_count"] #this is the followers of the user
    if user_following == None or user_followers==False:
        user_following = int(0)
    #print("Followers:",user_followers,"Following:",user_following)
    follower_impact=(min(user_followers,MAX_FOLLOWERS)/MAX_FOLLOWERS)*50 #this is the calculation for the follower impact
    ff_proportion = (user_followers/(user_followers+user_following))*50 # this is the calculation of proportion between follower and followin 

    social_credibility= follower_impact+ff_proportion
    return social_credibility

if __name__ == "__main__":
    f=open("/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/Tweets/sydneysiege-all-rnr-threads/rumours/544515538383564801/source-tweets/544515538383564801.json")
    data=json.load(f)

    user_cred=round(userCredibility(data),2)

    social_cred=round(socialCredibility(data),2)

    print("User Credibility ",user_cred, "Social Credibility ",social_cred)