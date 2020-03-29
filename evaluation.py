import chess

class EvalParams:
   
   def __init__(self):
      self.pawn_w = 10 
      self.knight_w = 30
      self.bishop_w = 30
      self.rook_w = 50
      self.queen_w = 90
      self.king_w = 900

def evaluateMaterial(board, params):
   wpval = params.pawn_w * len(board.pieces(chess.PAWN, chess.WHITE))
   bpval = -1 * params.pawn_w * len(board.pieces(chess.PAWN, chess.BLACK))

   wkval = params.knight_w * len(board.pieces(chess.KNIGHT, chess.WHITE))
   bkval = -1 * params.knight_w * len(board.pieces(chess.KNIGHT, chess.BLACK))

   wbval = params.bishop_w * len(board.pieces(chess.BISHOP, chess.WHITE))
   bbval = -1 * params.bishop_w * len(board.pieces(chess.BISHOP, chess.BLACK))

   wrval = params.rook_w * len(board.pieces(chess.ROOK, chess.WHITE))
   brval = -1 * params.rook_w * len(board.pieces(chess.ROOK, chess.BLACK))

   wqval = params.queen_w * len(board.pieces(chess.QUEEN, chess.WHITE))
   bqval = -1 * params.queen_w * len(board.pieces(chess.QUEEN, chess.BLACK))

   return wpval + bpval + wkval + bkval + wbval + bbval + wrval + brval + wqval + bqval

      

def evaluateBoard(board, params):
   if board.is_checkmate():
      if not board.turn:
         return 9999
      else:
         return -9999

   if board.is_game_over():
      return 0

   if board.turn:
      return evaluateMaterial(board, params) 
   else:
      return -1 * evaluateMaterial(board, params)

