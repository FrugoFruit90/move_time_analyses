import csv
import json

rows = []
gameClocks = []


def added_time_detected(clock_list):
    # takes one player's clocks and determines if there was added time encountered
    for i in range(0, len(clock_list) - 1):
        if (clock_list[i + 1] - clock_list[i]) > 60:
            return True
    return False


with open("clock_data_small.csv") as csvfile:
    filereader = csv.reader(csvfile)
    for row in filereader:
        rows.append(row)
    rows.pop(0)

for row in rows:
    # TODO: add checks for time control
    try:
        clocks = json.loads(row[18])
    except:
        print(row[3])
        continue
        # this happens if there's None in the clocks, which probably means that the data went missing somewhere
    white_clocks = clocks[::2]
    black_clocks = clocks[1::2]
    if not (added_time_detected(white_clocks) or added_time_detected(black_clocks)):
        gameClocks.append([white_clocks, black_clocks])
        # this means that time formats where there's added time encountered are removed
        # note that games in time formats where there's added time,
        # but the game didnt last long enough for time to be added are not filtered here!
