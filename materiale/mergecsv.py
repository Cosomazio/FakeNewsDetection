import pandas as pd
import numpy as np
import os
import csv

def mergecsv(csv_path,new_csv_path):
    f= open(new_csv_path,'a', encoding="UTF8")
    
    spam_df = pd.read_csv(csv_path, delimiter=',', header=None)
    
    text=spam_df[3]
    
    spam=spam_df[4]
    rows=[]
    writer = csv.writer(f,delimiter="\t")
    for i in range(1,len(text)):
        spams= "spam" if spam[i]=='1' else "ham"
        row = spams+",\t"+text[i]+"\n"
        rows.append(row)
        #print(type(row))
        #print(row)
        #writer.writerow(row)
    f.writelines(rows)
    
    
    f.close()


filepath="./FakeNewsDetection/materiale/YouTube-Spam-Collection-v1"
for path in os.listdir(filepath):
    #print(path)
    mergecsv(filepath+"/"+path,"spam_train2.csv")
    