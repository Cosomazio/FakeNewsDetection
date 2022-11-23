from feature_extraction.extractor import *
import csv
import os

if __name__ == '__main__':
    write_to_path= './test2.csv'
    v2_connection = api_v2_connection()
    v1_connection = api_v1_connection()
    for name in os.listdir("./RecentFakeNews_tweetID"):
        if(name !='sonictrans_id.txt'):
            continue
        else:
            print(name)
            with open("./RecentFakeNews_tweetID/"+name) as f:
                lines = f.readlines()
            
            with open(write_to_path, 'a') as f:
                writer = csv.writer(f, lineterminator="\n")
                c=0
                for i in range(len(lines)):
                    if(c==300):
                        break
                    line = str(lines[i].split('\n')[0])
                    sample = extraction(line, v2_connection, v1_connection)
                    if(sample is not None):
                        sample = np.append(sample, -1)
                        writer.writerow(sample)
                        print(i)
                        c+=1