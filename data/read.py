import chess.pgn
import random

def get_move(f):
    while True:
        game = chess.pgn.read_game(f)
        if not game:
            return None
        numOfMoves = int(game.headers['PlyCount'])
        # Skip short games
        if numOfMoves < 4:
            continue

        if game.headers["Result"] == '0-1':
            continue

        board = game.board()
        moves = iter(game.mainline_moves())
        for i in range(random.randint(1, numOfMoves-2)):
            move = next(moves)
            board.push(move)
        if not board.turn:
            board.push(next(moves))
        pre = board.copy(stack=False)
        board.push(next(moves))
        yield pre, board




