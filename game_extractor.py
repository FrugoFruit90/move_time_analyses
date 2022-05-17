import requests 
import ndjson
import lichessapitoken #this is a local file, you will have to put it locally w a token w study:read access- see README
apitoken=lichessapitoken.token #only gives study:read access
#print(apitoken)
#this gets tournaments which is a good start
headers={"Authentication": "Bearer "+apitoken,"Accept": "application/json"}
answerTournaments=requests.get(url="https://lichess.org/api/broadcast", headers=headers)
tournaments=answerTournaments.json(cls=ndjson.Decoder)
for tournament in tournaments:
    for round in tournament["rounds"]:
        #print(round)
        id=round["id"]
        
        rounddata=requests.get(url="https://lichess.org/api/broadcast/round/"+id+".pgn", headers=headers)
        with open("test.pgn","w") as testfile:
            testfile.write(rounddata.text)
        break
    break
