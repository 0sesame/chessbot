import chess
import random
import evaluation

evalParams = evaluation.EvalParams()

# alpha beta functions based heavily on psuedo-code from here:
# https://www.chessprogramming.org/Alpha-Beta

def alphaBetaMax(board, alpha, beta, depthLeft):
   if depthLeft == 0:
      return evaluation.evaluateBoard(board, evalParams)

   for move in board.legal_moves:
      board.push(move)
      score = alphaBetaMin(board, alpha, beta, depthLeft - 1)
      board.pop()
      if score >= beta:
         return beta
      if score > alpha:
         alpha = score

   return alpha

def alphaBetaMin(board, alpha, beta, depthLeft):
   if depthLeft == 0:
      return evaluation.evaluateBoard(board, evalParams)

   for move in board.legal_moves:
      board.push(move)
      score = alphaBetaMax(board, alpha, beta, depthLeft - 1)
      board.pop()
      if score <= alpha:
         return alpha
      if score < beta:
         beta = score

   return beta

def get_move(board):
   best_score = -9999
   beta = 9999
   alpha = -9999
   depth = 1

   for move_to_eval in board.legal_moves:
      board.push(move_to_eval)
      move_score = alphaBetaMax(board, alpha, beta, 3)
      if move_score >= best_score:
         best_score = move_score
         best_move = move_to_eval
      board.pop()
   
   return best_move

def make_move(board):
   board.push(get_move(board))

def make_random_move(board):
   legal_moves = [move for move in board.legal_moves]
   board.push(legal_moves[random.randint(0, len(legal_moves) - 1)])

if __name__ == "__main__":
   board = chess.Board()
   while(not board.is_game_over()):
      if(board.turn):
         print("white move")
         make_move(board)
      else:
         print("black random move")
         make_random_move(board)
      print(board)
      print("------------------------------------")

   print(board.result())
   print('Is stalemate: {0}'.format(board.is_stalemate()))
   print('Is insufficient: {0}'.format(board.is_insufficient_material()))
   print('Is fivefold: {0}'.format(board.is_fivefold_repetition()))

