from datetime import date
from feature_extraction.twitter_api import *


SOCIALPLATFORMCREATED = 2006  #Year of creation of Twitter

def registration_age(user):
    if hasattr(user, "created_at"):
        return str(user.created_at).split()[0]
    else: return 0


def userCredibility(tweet_id):
    user = get_utente(tweet_id,api_v2_connection(),api_v1_connection())
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


