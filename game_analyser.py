import csv
import re
import json
rows  = []
gameClocks = []

def addedTimeDetector(clockList):
    #takes one player's clocks and determines if there was added time encountered
    for i in range(0,len(clockList)-1):
        if (clockList[i+1] - clockList[i]) > 60:
            return True
    return False
with open("clock_data_small.csv") as csvfile:
    filereader = csv.reader(csvfile)
    for row in filereader:
        rows.append(row)
    rows.pop(0)

for row in rows:
    #TODO: add checks for time control
    try:
        clocks = json.loads(row[18])
    except:
        print(row[3])
        continue; 
        #this happens if there's None in the clocks, which probably means that the data went missing somewhere
    whiteclocks = clocks[::2]
    blackclocks = clocks[1::2]
    if not (addedTimeDetector(whiteclocks) or addedTimeDetector(blackclocks)):
        gameClocks.append([whiteclocks,blackclocks])
        #this means that time formats where there's added time enountered are removed
        #note that games in time formats where there's added time, 
        #but the game didnt last long enough for time to be added are not filtered here!
    
    
    
