import json

writeto=[]
with open('28Ott4Nov.json') as f:
    data=json.load(f)

for el in data:
    print(el['full_text'])

    el['label']=str(input())
    writeto.append(el)
    

with open('28Ott4Nov1.json') as f:
   data = json.load(f)

for el in data:
    print(el['id'], '\n', el['full_text'])

    el['label']=str(input())
    writeto.append(el)

print('sto scrivendo il file')

with open('28Ott4NovDef.json', 'w') as f:
    json.dump(writeto, f, indent=5)
