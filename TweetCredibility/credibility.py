from tkinter.tix import Tree
from socialCredibility import socialCredibility
from userCredibility import userCredibility
from textCredibility import textCredibility

import os
from tqdm import tqdm

def credibility(tweetPath, social_weight=0.33, user_weight=0.33, text_weight=0.34):
    cred = textCredibility(tweetPath)*text_weight+userCredibility(tweetPath)*user_weight+socialCredibility(tweetPath)*social_weight
    return True if cred>50 else False


if __name__=="__main__":
    dataset_path="../DATASET/all-rnr-annotated-threads"
    non_rumor=[]
    rumor=[]

    rumor_creds=[]
    non_rumor_creds=[]

    for name in tqdm(os.listdir(dataset_path)):
        if name == ".DS_Store":
            continue
        path_non_rumor=dataset_path+"/"+name+"/non-rumours"
        for tweet_dir in os.listdir(path_non_rumor):
            if tweet_dir == ".DS_Store":
                continue
            file = path_non_rumor + "/"+tweet_dir+"/source-tweets/"+tweet_dir+".json"
            non_rumor.append(file)

        path_rumor=dataset_path+"/"+name+"/rumours"
        for tweet_dir in os.listdir(path_rumor):
            if tweet_dir == ".DS_Store":
                continue
            file = path_rumor + "/"+tweet_dir+"/source-tweets/"+tweet_dir+".json"
            rumor.append(file)
    
    print(len(rumor), len(non_rumor))

    for el in tqdm(rumor):
        rumor_creds.append(credibility(el))
    for el in non_rumor:
        non_rumor_creds.appen(credibility(el))
    
    miss_rumor=0
    for el in tqdm(rumor_creds):
        if(el == True):
            miss_rumor+=1
    
    miss_non_rumor=0
    for el in tqdm(non_rumor_creds):
        if el ==False:
            miss_non_rumor+=1

    print("MISS RUMOR, MISS NON RUMOR, RUMORS, NON RUMORS, MISS RUMOR PERC, MISS NON RUMOR PERC")
    print(miss_rumor, miss_non_rumor, len(rumor), len(non_rumor), miss_rumor/len(rumor), miss_non_rumor/len(non_rumor))

    


