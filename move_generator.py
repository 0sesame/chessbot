import chess
import random
import evaluation


# alphaBeta Negamax implementation based heavily on psuedo-code from here:
# https://www.chessprogramming.org/Alpha-Beta

# Quiesence search function based heavily on psuedo-code from here:
# https://www.chessprogramming.org/Quiescence_Search

def quiesence(board, params, alpha, beta):
   stand_pat = evaluation.evaluateBoard(board, params)
   if stand_pat >= beta:
      return beta
   if stand_pat > alpha:
      alpha = stand_pat
   
   for move in board.legal_moves:
      if board.is_capture(move):
         board.push(move)
         score = -1 * quiesence(board, params, -1 * alpha, -1 * beta)
         board.pop()
         if score >= beta:
            return beta
         if score > alpha:
            alpha = score

   return alpha 

def alphaBeta(board, params, alpha, beta, depthLeft):
   if depthLeft == 0:
      return quiesence(board, params, alpha, beta)

   for move in board.legal_moves:
      board.push(move)
      score = -1 * alphaBeta(board, params, -1 * alpha, -1 * beta, depthLeft - 1)
      board.pop()
      if score >= beta:
         return beta
      if score > alpha:
         alpha = score

   return alpha

def generate_move(board, params):
   best_score = -9999
   beta = 9999
   alpha = -9999
   depth = 1

   for move_to_eval in board.legal_moves:
      board.push(move_to_eval)
      move_score = alphaBeta(board, params, alpha, beta, depth - 1)
      if move_score >= best_score:
         best_score = move_score
         best_move = move_to_eval
      board.pop()
   
   return best_move

def make_move(board, params):
   board.push(generate_move(board, params))

def make_random_move(board):
   legal_moves = [move for move in board.legal_moves]
   board.push(legal_moves[random.randint(0, len(legal_moves) - 1)])

if __name__ == "__main__":
   win ="1-0"
   loss = "0-1"
   ties = "1/2 - 1/2"
   wins = 0
   losses = 0
   ties = 0
   params = evaluation.EvalParams(False)
   for i in range(20):
      board = chess.Board()
      while(not board.is_game_over()):
         if(board.turn):
            print("white move")
            make_move(board, params)
         else:
            print("black random move")
            make_random_move(board)
         print(board)
         print("------------------------------------")
      if board.result() == win:
         wins += 1
      elif board.result() == loss:
         losses += 1
      else:
         ties += 1

   print("wins: {0}   losses: {1}    ties: {2}".format(wins, losses, ties))
   print('Is stalemate: {0}'.format(board.is_stalemate()))
   print('Is insufficient: {0}'.format(board.is_insufficient_material()))
   print('Is fivefold: {0}'.format(board.is_fivefold_repetition()))

