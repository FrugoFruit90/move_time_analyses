import logging
from typing import Generator, TextIO, Callable

import chess.pgn
from chess.pgn import ResultT, BaseVisitor, CLOCK_REGEX, GameBuilder

logging.getLogger("chess.pgn").setLevel(logging.CRITICAL)


def load_games_from_pgn(pgn_file: TextIO, visitor: Callable[[], BaseVisitor[ResultT]] = GameBuilder) -> \
        Generator[chess.pgn.Game, None, None]:
    while True:
        next_game = chess.pgn.read_game(pgn_file, Visitor=visitor)
        if not next_game:
            break
        yield next_game


def load_headers_from_pgn(pgn_file: TextIO) -> Generator[chess.pgn.Headers, None, None]:
    while True:
        next_game = chess.pgn.read_headers(pgn_file)
        if not next_game:
            break
        yield next_game
