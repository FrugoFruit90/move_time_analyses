import argparse
import pandas as pd

from loaders import load_games_from_pgn

parser = argparse.ArgumentParser()
parser.add_argument('pgn_file', type=argparse.FileType('r'))
parser.add_argument('--n_games', type=int, default=None)
args = parser.parse_args()

game_data = []
for i, game in enumerate(load_games_from_pgn(args.pgn_file)):
    if args.n_games is not None and len(game_data) >= args.n_games:
        break
    headers = dict(game.headers)
    try:
        start_time_white = game.next().clock()
    except AttributeError:
        continue
    if start_time_white is None or game.next().clock() < 5000:
        continue
    else:
        clock_values = []
        moves = []
        for move in game.mainline():
            clock_values.append(move.clock())
        headers['clocks'] = clock_values
        headers['moves'] = str(game.mainline())
        game_data.append(headers)
pd.DataFrame(game_data).to_csv("clock_data.csv", index=False)
