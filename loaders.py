from typing import Generator, TextIO

import chess.pgn


def load_games_from_pgn(pgn_file: TextIO) -> Generator[chess.pgn.Game, None, None]:
    while True:
        next_game = chess.pgn.read_game(pgn_file)
        if not next_game:
            break
        yield next_game
