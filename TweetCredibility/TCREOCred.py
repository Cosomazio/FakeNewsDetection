# from socialCredibility import socialCredibility
# from userCredibility import userCredibility
from textCredibility import textCredibility
import sys
from datetime import date
#import ray
from feature_extraction.twitter_api import *
MAX_FOLLOWERS = 132500000  #max number of follower on Twitter (Barak Obama)
SOCIALPLATFORMCREATED = 2006  #Year of creation of Twitter


def socialCredibility(user):
    # user_following = data["user"]["following"] #this is the following of the user
    # user_followers= data["user"]["followers_count"] #this is the followers of the user
    
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


def registration_age(user):
    if hasattr(user, "created_at"):
        return str(user.created_at).split()[0]
    else: return 0


def userCredibility(user):
    if user == None:
        return None
    verified_weight=50 if verified(user) else 0 #this is for see if the user is verfied
    creation_data=registration_age(user)
    #this is the calculation for the age of the profile --> currentYear - YearJoined
    account_age= date.today().year - int(creation_data.split("-")[0])
    #this is the calculation for the max account age for one profile in Twitter --> currentYear - YearSocialPlatformCreated
    max_account_age= date.today().year - SOCIALPLATFORMCREATED 
    creation_weight=(account_age/max_account_age)* 50 
    
    user_credibility= verified_weight + creation_weight
    return user_credibility



def credibility(tweetid,nlp = False, social_weight=0.30, user_weight=0.35, text_weight=0.35): #i pesi di base sono 0.33,0.33,0.34

    user = get_utente(tweetid,api_v2_connection(),api_v1_connection())
    nlp = True if nlp=="True" else False
    text_cred=textCredibility(tweetid, NLP = nlp)
    user_cred=userCredibility(user)
    social_cred=socialCredibility(user)

    #!Ci mette troppo tempo quando parallelizzo
    # x=twcred.remote(tweetid)
    # y=uscred.remote(tweetid)
    # z=sccred.remote(tweetid)

    #text_cred,user_cred,social_cred = ray.get([x,y,z])
    
    if text_cred == None or user_cred==None or social_cred == None:
        return None
    #print(text_cred,user_cred,social_cred)
    cred = text_cred*text_weight+user_cred*user_weight+social_cred*social_weight
    return cred

# @ray.remote
# def twcred(tweetid):
#     return textCredibility(tweetid)

# @ray.remote
# def uscred(tweetid):
#     return userCredibility(tweetid)

# @ray.remote
# def sccred(tweetid):
#     return socialCredibility(tweetid)

if __name__ == "__main__":
    id = sys.argv
    print(credibility(id[1],id[-1]))
    
     