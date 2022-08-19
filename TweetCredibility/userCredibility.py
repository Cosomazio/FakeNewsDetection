from datetime import date
import json

SOCIALPLATFORMCREATED = 2006  #Year of creation of Twitter

def userCredibility(filepath):
    data=getdata(filepath)
    user=data["user"]
    
    verified_weight=50 if user["verified"] else 0 #this is for see if the user is verfied

    creation_data=data["created_at"].split()
    #this is the calculation for the age of the profile --> currentYear - YearJoined
    account_age= date.today().year- int(creation_data[len(creation_data)-1]) 
    #this is the calculation for the max account age for one profile in Twitter --> currentYear - YearSocialPlatformCreated
    max_account_age= date.today().year - SOCIALPLATFORMCREATED 
    creation_weight=(account_age/max_account_age)* 50 

    user_credibility= verified_weight + creation_weight
    return user_credibility


def getdata(filepath):
    f=open(filepath)
    data = json.load(f)
    f.close()
    return data
