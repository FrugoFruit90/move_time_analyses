import argparse

import pandas as pd

from loaders import load_headers_from_pgn

parser = argparse.ArgumentParser()
parser.add_argument('pgn_file', type=argparse.FileType('r'))
args = parser.parse_args()

headers = load_headers_from_pgn(args.pgn_file)
header_df = pd.DataFrame(headers)
print(header_df.TimeControl.value_counts(dropna=False))
