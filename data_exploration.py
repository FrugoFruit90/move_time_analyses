import argparse

import chess.pgn
import pandas as pd

from loaders import load_games_from_pgn

parser = argparse.ArgumentParser()
parser.add_argument('pgn_file', type=argparse.FileType('r'))
args = parser.parse_args()

games = load_games_from_pgn(args.pgn_file)
headers = [game.headers for game in games]
header_df = pd.DataFrame(headers)
print(header_df.TimeControl.value_counts(dropna=False))
