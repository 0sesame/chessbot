import chess
import random
import chess.svg





def get_move(board):
   legal_moves = [move for move in board.legal_moves]

   return legal_moves[random.randint(0, len(legal_moves) - 1)]

def make_move(board):
   board.push(get_move(board))

if __name__ == "__main__":
   board = chess.Board()
   while(not board.is_game_over()):
      make_move(board) 
      print(board)
      print("------------------------------------")
   print(board.result())
