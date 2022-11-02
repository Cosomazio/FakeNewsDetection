
from xgboost import XGBRegressor
from xgboost import XGBClassifier
import pandas as pd
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score



#!LOAD THE FIRST TEST SET  FAKENEWSNET
file_path = "/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/TweetCredibility/csv/dataset_fake.csv"

x_test=[]
y_test=[]
with open(file_path, newline='\n') as f:
            reader = csv.reader(f,delimiter=";")
            #header = next(reader)
            for row in reader:
                    #print(row)
                    x_test.append(row[1:-1])
                    y_test.append(row[-1])

file_path = "/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/TweetCredibility/csv/dataset_real.csv"
with open(file_path, newline='\n') as f:
            reader = csv.reader(f,delimiter=";")
            #header = next(reader)
            for row in reader:
                    #print(row)
                    x_test.append(row[1:-1])
                    y_test.append(row[-1])

                    
x_test= np.array(x_test,dtype='float')
y_test = np.array(y_test,dtype='int')

#!LOAD THE SECOND TEST SET
x1_test=[]
y1_test=[]
filepath="/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/TweetCredibility/csv/features.csv"
with open(filepath, newline='\n') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                    #print(row)
                    x1_test.append(row[1:-1])
                    y1_test.append(row[-1])
x1_test= np.array(x1_test,dtype='float')
y1_test = np.array(y1_test,dtype='int')

#!LOAD THE TRAINING SET
file_path = "/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/TweetCredibility/csv/feature_imageverification.csv"

x_train=[]
y_train=[]
with open(file_path, newline='\n') as f:
            reader = csv.reader(f,delimiter=";")
            #header = next(reader)
            for row in reader:
                    #print(row)
                    x_train.append(row[1:-1])
                    y_train.append(row[-1])

x_train= np.array(x_test,dtype='float')
y_train = np.array(y_test,dtype='int')
X_train, X_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2,random_state=0)

#!XGBOOST CLASSIFIER
model = XGBClassifier(n_estimators=1000,objective="binary:logistic",base_score=0.9,learning_rate=0.01,max_depth=10)
model.fit(X_train, y_train)
y_pred = model.predict(X_val)
print("CLASSIFIER")
print("RESULT ON A VALIDATION")
print("Accuracy: ",accuracy_score(y_val, y_pred))
print("Precision: ",precision_score(y_val, y_pred,zero_division=0))
print("Recall: ",recall_score(y_val, y_pred,zero_division=0))
print(confusion_matrix(y_val, y_pred))
print("RESULT ON A FAKENEWSNET")
y_pred = model.predict(x_test)
print("Accuracy: ",accuracy_score(y_test, y_pred))
print("Precision: ",precision_score(y_test, y_pred,zero_division=0))
print("Recall: ",recall_score(y_test, y_pred,zero_division=0))
print(confusion_matrix(y_test, y_pred))
print("RESULT ON A SECOND DATASET TEST")
y1_pred = model.predict(x1_test)
print("Accuracy: ",accuracy_score(y1_test, y1_pred))
print("Precision: ",precision_score(y1_test, y1_pred,zero_division=0))
print("Recall: ",recall_score(y1_test, y1_pred,zero_division=0))
print(confusion_matrix(y1_test, y1_pred))

#!XGBOOST REGRESSOR
model = XGBRegressor(n_estimators=1000, max_depth=5, eta=0.1,base_score=0.1,subsample=0.7, colsample_bytree=0.8,random_state=1)
model.fit(X_train, y_train)
y_pred = model.predict(X_val)
for i in range(y_pred.shape[0]):
        if y_pred[i] < 0.5:
            y_pred[i] = 0
        else:
            y_pred[i] = 1
print("REGRESSOR")
print("RESULT ON A VALIDATION")          
print("Accuracy: ",accuracy_score(y_val, y_pred))
print("Precision: ",precision_score(y_val, y_pred,zero_division=0))
print("Recall: ",recall_score(y_val, y_pred,zero_division=0))
print(confusion_matrix(y_val, y_pred))

y_pred = model.predict(x_test)
for i in range(y_pred.shape[0]):
        if y_pred[i] < 0.5:
            y_pred[i] = 0
        else:
            y_pred[i] = 1
print("RESULT ON A FAKENEWSNET")
print("Accuracy: ",accuracy_score(y_test, y_pred))
print("Precision: ",precision_score(y_test, y_pred,zero_division=0))
print("Recall: ",recall_score(y_test, y_pred,zero_division=0))
print(confusion_matrix(y_test, y_pred))

y1_pred = model.predict(x1_test)
for i in range(y1_pred.shape[0]):
        if y1_pred[i] < 0.5:
            y1_pred[i] = 0
        else:
            y1_pred[i] = 1
print("RESULT ON A SECOND DATASET TEST")
print("Accuracy: ",accuracy_score(y1_test, y1_pred))
print("Precision: ",precision_score(y1_test, y1_pred,zero_division=0))
print("Recall: ",recall_score(y1_test, y1_pred,zero_division=0))
print(confusion_matrix(y1_test, y1_pred))
