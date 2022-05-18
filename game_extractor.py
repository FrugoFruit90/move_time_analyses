import requests 
import ndjson
import lichessapitoken #this is a local file, you will have to put it locally w a token w study:read access- see README
import time
import codecs
apitoken=lichessapitoken.token #only gives study:read access
#print(apitoken)
#this gets tournaments which is a good start
headers={"Authentication": "Bearer "+apitoken,"Accept": "application/json"}
answerTournaments=requests.get(url="https://lichess.org/api/broadcast", headers=headers, params={"nb":50})
tournaments=answerTournaments.json(cls=ndjson.Decoder)
print(len(tournaments))
x=0
for tournament in tournaments:
    x=x+1
    for round in tournament["rounds"]:
        #print(round)
        id=round["id"]
        print("requesting")
        rounddata=requests.get(url="https://lichess.org/api/broadcast/round/"+id+".pgn", headers=headers)
        print("requested")
        if(rounddata.status_code==429):
            print("rate limited")
            time.sleep(61)
            print("going again")
            rounddata=requests.get(url="https://lichess.org/api/broadcast/round/"+id+".pgn", headers=headers)
        if("%clk" not in rounddata.text):
            continue;
        with codecs.open("test.pgn","a", "utf-8") as testfile:
            testfile.write(rounddata.text)
        print("round done")
    print(f"tournament {x} done")
    

