import pickle as pk
from feature_extraction.extractor import *
import sys

""" trained model for fake news detection"""
def load_model(path):
    return pk.load(open(path, 'rb'))

"""extraction of feature vector from tweet ID"""
def feat_vect(ID):
    v2_connection = api_v2_connection()
    v1_connection = api_v1_connection()
    return extraction(ID, v2_connection, v1_connection)

""" this module detect if a certain tweet, given its id is fake or not"""
if __name__=="__main__":
    id =int(sys.argv[1])
    model = load_model("./models/xgbmodel")
    fv=feat_vect(id)
    
    if fv is None:
        sys.exit(-1)
        
    fv=fv.reshape(1, 57)
    prediction = model.predict(fv)
    if(prediction==1):
        sys.exit(10)
        
    else:
        sys.exit(-10)

    