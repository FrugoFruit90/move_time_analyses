import argparse
import datetime

import numpy as np
import pandas as pd

from loaders import load_games_from_pgn


def np_array_shift(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


parser = argparse.ArgumentParser()
parser.add_argument('pgn_file', type=argparse.FileType('r'))
parser.add_argument('--time_control_40', action='store_true')
parser.add_argument('--time_control_60', action='store_true')
parser.add_argument('--n_games', type=int, default=None)
args = parser.parse_args()

game_data = []
for i, game in enumerate(load_games_from_pgn(args.pgn_file)):
    try:
        if args.n_games is not None and len(game_data) >= args.n_games:
            break
        headers = dict(game.headers)
        try:
            start_time_white = game.next().clock()
            start_time_black = game.next().next().clock()
        except AttributeError:
            continue
        if start_time_white is None or start_time_black is None or not 5500 > max(start_time_white,
                                                                                  start_time_black) > 5300:
            continue
        else:
            clock_values = []
            moves = []
            for move in game.mainline():
                clock_values.append(move.clock())
            clocks = clock_values
            if any(map(lambda x: x is None, clocks)):
                continue
            headers['WhiteClocks'] = clocks[::2]
            headers['BlackClocks'] = clocks[1::2]
            time_usage_white = np_array_shift(headers['WhiteClocks'], 1) - np.array(headers['WhiteClocks'])
            time_usage_black = np_array_shift(headers['BlackClocks'], 1) - np.array(headers['BlackClocks'])
            try:
                if np.nanmin(np.delete(time_usage_white, 39)) < -30 or np.nanmin(
                        np.delete(time_usage_black, 39)) < -30:
                    continue
                if args.time_control_40 != time_usage_white[39] < -200:
                    continue
                if args.time_control_60 != time_usage_white[59] < -200:
                    continue
            except IndexError:
                if np.nanmin(time_usage_white) < -30 or np.nanmin(time_usage_black) < -30:
                    continue
            game_data.append(headers)
    except Exception as exception:
        print(f"error while processing game {i}, exception: {exception}")

now = datetime.datetime.now()
pd.DataFrame(game_data).to_csv(f"clock_data_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.csv", index=False)
