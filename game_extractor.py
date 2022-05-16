import requests 
import ndjson
import lichessapitoken #this is a local file, you will have to put it locally w a token w study:read access- see README
apitoken=lichessapitoken.token #only gives study:read access
print(apitoken)
#this gets tournaments which is a good start
headers={"Authorization": 'Bearer "+apitoken'}
answerTournaments=requests.get(url="https://lichess.org/api/broadcast", headers=headers)
tournaments=answerTournaments.json(cls=ndjson.Decoder)
for tournament in tournaments:
    for round in tournament["rounds"]:
        print(round)
        id=round["id"]
        
        rounddata=requests.get(url="https://lichess.org/api/broadcast/-/-/"+id)
        print(rounddata.url)
        #print(rounddata.text)
        break
    break