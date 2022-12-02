
import json
from tqdm import tqdm
from functools import partial
from geopy import Nominatim
from geopy.geocoders import Nominatim
import pysolr

def location(nameLoc):
    loc = Nominatim(user_agent="GetLoc")
    #entering the location name
    geocode = partial(loc.geocode, language="es")
    getLoc = geocode(nameLoc)
    #print("long: ",getLoc.longitude," lat: ",getLoc.latitude,"name: ",getLoc.address)
    return((getLoc.latitude,getLoc.longitude))
    
def mostlocation(locName,coord):
    latitude = coord[0]
    longitude = coord[1]
    # if locName == "Earth":
    #     locName = "New York"
    #     latitude=40.779897
    #     longitude=-73.968565
    
    node={
        "type":"node",
        "labels":["Tweet"],
        "properties":{"coordinates":[latitude,longitude],"name":str(locName),"latitude":latitude,"longitude":longitude,"crs":'WGS-84'}
    }
    json_object = json.dumps(node)
    with open("/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/CommunityDetection/noteTweet.json","a") as file:
        file.write(json_object+"\n")
            

    
if __name__ == "__main__":
   
    solr = pysolr.Solr("http://193.205.163.45:2222/solr/FakeTweetsCC/",auth=("unisa","G4nd4lf"))
    
    num_fake = 44998 #!Constant value of Fake tweets present in the solr database
    res = solr.search("label_b:False",rows=num_fake)

    count = 0
    count_bad = 0
    for el in tqdm(res):
        try:
            locName = el['location_s']
            id = el['id']
            
            if locName == "Void":
                continue
            else:
                #print(el['location_s'])
                coord = location(locName)
                mostlocation(locName,coord)
                #print("Current element in the query result: ",count)
                count+=1
            
        except:
            count_bad+=1
            continue
    print(count,"   ",count_bad)
    
