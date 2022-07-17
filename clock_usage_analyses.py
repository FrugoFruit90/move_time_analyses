import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RELEVANT_COLUMNS = ["White", "WhiteElo", "WhiteTitle", "WhiteClocks", "Black", "BlackElo", "BlackTitle",
                    "BlackClocks", "Result"]


def get_result_from_perspective(x, colour):
    if x['Result'] == '1/2-1/2' or x['Result'] == '1/2':
        return 0.5
    elif x['Result'] == '1-0':
        if colour == 'black':
            return 0.0
        else:
            return 1.0
    elif x['Result'] == '0-1':
        if colour == 'black':
            return 1.0
        else:
            return 0.0
    else:
        return np.NaN


def tolerant_mean(arrs):
    """
    :param arrs:
    :return: per move number: average time left, std error, count
    """
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens), len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l), idx] = l
    return np.nanmean(arr, axis=-1), arr.std(axis=-1), arr.count(axis=-1)


parser = argparse.ArgumentParser()
parser.add_argument('csv_file', type=argparse.FileType('r'))
args = parser.parse_args()

game_data = pd.read_csv(args.csv_file, converters={'BlackClocks': pd.eval, 'WhiteClocks': pd.eval})

game_data['WhiteElo'] = pd.cut(game_data['WhiteElo'], bins=np.arange(31) * 100)
game_data['BlackElo'] = pd.cut(game_data['BlackElo'], bins=np.arange(31) * 100)
game_data_white = game_data[RELEVANT_COLUMNS].rename(
    columns={
        "White": "Name",
        "WhiteElo": "Elo",
        "WhiteTitle": "Title",
        "WhiteClocks": "Clocks",
        "Black": "OppName",
        "BlackElo": "OppElo",
        "BlackTitle": "OppTitle",
        "BlackClocks": "OppClocks"
    })
game_data_white["Result"] = game_data_white.apply(get_result_from_perspective, args=("white",), axis=1)

game_data_black = game_data[RELEVANT_COLUMNS].rename(
    columns={
        "White": "OppName",
        "WhiteElo": "OppElo",
        "WhiteTitle": "OppTitle",
        "WhiteClocks": "OppClocks",
        "Black": "Name",
        "BlackElo": "Elo",
        "BlackTitle": "Title",
        "BlackClocks": "Clocks"
    })
game_data_black["Result"] = game_data_black.apply(get_result_from_perspective, args=("black",), axis=1)
player_perspective_data = pd.concat([game_data_white, game_data_black], axis=0)
player_perspective_data = player_perspective_data.dropna(subset=['Result'])

mask = player_perspective_data['Elo'].value_counts() > 100

fig, ax = plt.subplots()
for rating_group in player_perspective_data['Elo'].value_counts()[mask].index.to_list():
    list_of_ys_diff_len = player_perspective_data[player_perspective_data['Elo'] == rating_group]['Clocks'].to_list()
    means, stds, counts = tolerant_mean(list_of_ys_diff_len)
    ax.plot(np.arange(len(means)) + 1, means, label=rating_group)
ax.legend()
plt.savefig("time_usage.png")
