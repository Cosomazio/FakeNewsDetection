import numpy as np
import pandas as pd
import numpy as np
import csv

from extractor import *

"""this module is used to prepare the training set used to train the XGBOOST module for our fake news detection backend"""
if __name__ == "__main__":
    path_fake = "./FakeNewsNet/fake.csv"
    path_real = "./FakeNewsNet/real.csv"

    write_to_path = "./FakeNewsNet/real_with_feat.csv"

    ids = []
    data=[]
    labels=[]

    v2_connection = api_v2_connection()
    v1_connection = api_v1_connection()

    with open(path_real, 'r') as f:
        reader = csv.reader(f)
        for el in reader:
            ids.append(el)
    
    with open(write_to_path, 'a') as f:
        writer = csv.writer(f, lineterminator="\n")
        for i in range(6152, len(ids)):

            sample = extraction(ids[i][0], v2_connection, v1_connection)
            if(sample is not None):
                sample = np.append(sample, -1)
                writer.writerow(sample, )
                print(i)