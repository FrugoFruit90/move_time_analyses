import requests
import ndjson
import \
    lichessapitoken  # this is a local file, you will have to put it locally w a token w study:read access- see README
import time
import codecs
NUMBER_OF_TOURNAMENTS=100 #how many tournaments to analyze
api_token = lichessapitoken.token  # only gives study:read access
# print(api_token)
# this gets tournaments which is a good start
headers = {"Authentication": "Bearer " + api_token, "Accept": "application/json"}
answerTournaments = requests.get(url="https://lichess.org/api/broadcast", headers=headers, params={"nb": NUMBER_OF_TOURNAMENTS})
tournaments = answerTournaments.json(cls=ndjson.Decoder)
print(len(tournaments))
x = 0
for tournament in tournaments:
    x = x + 1
    for tournament_round in tournament["rounds"]:
        # print(round)
        round_id = tournament_round["id"]
        print("requesting")
        round_data_url = f"https://lichess.org/api/broadcast/round/{round_id}.pgn"
        round_data = requests.get(url=round_data_url, headers=headers)
        print("requested")
        if round_data.status_code == 429:
            print("rate limited")
            time.sleep(61)
            print("going again")
            round_data = requests.get(url=round_data_url, headers=headers)
        if "%clk" not in round_data.text:
            continue
        with codecs.open("test.pgn", "a", "utf-8") as testfile:
            testfile.write(round_data.text)
        print("round done")
    print(f"tournament {x} done")
