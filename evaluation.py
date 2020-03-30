import chess
import random

PAWN_W = 0
KNIGHT_W = 1
BISHOP_W = 2
ROOK_W = 3
QUEEN_W = 4
KING_W = 5
DOUBLED_PAWN_PENALTY = 6
PASSED_PAWNS = 7
ROOK_HOR_MOBILITY = 8
ROOK_VERT_MOBILITY = 9

class EvalParams:
   
   def __init__(self, randomize):
      self.fitness = 0
      self.params = [10, 30, 30, 50, 90, 900, 14, 5, 5, 20]
      self.param_c = len(self.params)
      
      if randomize == True:
         self.randomize_weights()
   
   def randomize_weights(self):
      self.params = [random.randint(0, 2500) for _ in range(self.param_c)]
   

def on_board(pos):
   return 0 <= pos and pos <= 63

def get_rook_possible_vert_moves(board, rook):
   possible_moves = 0
   curr = rook - 8
   while (on_board(curr) and chess.square_file(curr) == chess.square_file(rook)
         and board.piece_at(curr) != None):
      possible_moves += 1 
      curr -= 8
   
   curr = rook + 8
   while (on_board(curr) and chess.square_file(curr) == chess.square_file(rook)
         and board.piece_at(curr) != None):
      possible_moves += 1 
      curr += 8

   return possible_moves

def get_rook_possible_hor_moves(board, rook):
   possible_moves = 0
   curr = rook - 1
   while (on_board(curr) and chess.square_rank(curr) == chess.square_rank(rook)
         and board.piece_at(curr) != None):
      possible_moves += 1 
      curr -= 1
   
   curr = rook + 1
   while (on_board(curr) and chess.square_rank(curr) == chess.square_rank(rook)
         and board.piece_at(curr) != None):
      possible_moves += 1 
      curr += 1
   
   return possible_moves
   
def evaluate_rook_mobility(board, params):
   white_rooks = board.pieces(chess.ROOK, chess.WHITE)
   black_rooks = board.pieces(chess.ROOK, chess.BLACK)
  
   white_hor_mobility = 0 
   white_vert_mobility = 0 
   for rook in list(white_rooks):
      white_hor_mobility += get_rook_possible_hor_moves(board, rook) 
      white_vert_mobility += get_rook_possible_vert_moves(board, rook) 

   black_hor_mobility = 0 
   black_vert_mobility = 0 
   for rook in list(black_rooks):
      black_hor_mobility += get_rook_possible_hor_moves(board, rook) 
      black_vert_mobility += get_rook_possible_vert_moves(board, rook) 

   return (params[ROOK_HOR_MOBILITY]*(white_hor_mobility - black_hor_mobility) +
           params[ROOK_VERT_MOBILITY]*(white_vert_mobility - black_vert_mobility))
         
   
def evaluate_doubled_passed_pawns(board, params):
   white_doubled = 0
   black_doubled = 0
   for fil in range(len(chess.FILE_NAMES)):
      wpc = 0
      bpc = 0
      for rank in range(len(chess.RANK_NAMES)):
         piece = board.piece_at(chess.square(fil, rank))
         if piece != None and piece.piece_type == chess.PAWN:
            if piece.color:
               wpc += 1
            else:
               bpc += 1
      if wpc > 1:
         white_doubled += 1
      if bpc > 1:
         black_doubled += 1 

   return -1 * params[DOUBLED_PAWN_PENALTY] * (white_doubled - black_doubled)


def evaluateMaterial(board, params):
   wpval = params[PAWN_W] * len(board.pieces(chess.PAWN, chess.WHITE))
   bpval = -1 * params[PAWN_W] * len(board.pieces(chess.PAWN, chess.BLACK))

   wkval = params[KNIGHT_W] * len(board.pieces(chess.KNIGHT, chess.WHITE))
   bkval = -1 * params[KNIGHT_W] * len(board.pieces(chess.KNIGHT, chess.BLACK))

   wbval = params[BISHOP_W] * len(board.pieces(chess.BISHOP, chess.WHITE))
   bbval = -1 * params[BISHOP_W] * len(board.pieces(chess.BISHOP, chess.BLACK))

   wrval = params[ROOK_W] * len(board.pieces(chess.ROOK, chess.WHITE))
   brval = -1 * params[ROOK_W] * len(board.pieces(chess.ROOK, chess.BLACK))

   wqval = params[QUEEN_W] * len(board.pieces(chess.QUEEN, chess.WHITE))
   bqval = -1 * params[QUEEN_W] * len(board.pieces(chess.QUEEN, chess.BLACK))

   wkival = params[KING_W] * len(board.pieces(chess.KING, chess.WHITE))
   bkival = params[KING_W] * len(board.pieces(chess.KING, chess.BLACK))

   return (wpval + bpval + wkval + bkval + wbval + bbval 
         + wrval + brval + wqval + bqval + wkival + bkival)

      

def evaluateBoard(board, params):
   if board.is_checkmate():
      if not board.turn:
         return 9999
      else:
         return -9999

   if board.is_game_over():
      return 0

   evaluation = (evaluateMaterial(board, params.params) 
               + evaluate_doubled_passed_pawns(board, params.params)
               + evaluate_rook_mobility(board, params.params))

   if board.turn:
      return evaluation
   else:
      return -1 * evaluation

