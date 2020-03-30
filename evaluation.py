import chess

class EvalParams:
   
   def __init__(self, randomize):
      self.pawn_w = 10 
      self.knight_w = 30
      self.bishop_w = 30
      self.rook_w = 50
      self.queen_w = 90
      self.king_w = 900
      
      self.doubled_pawn_penalty = 14
      self.passwed_pawns = 5
      
      if randomize == True:
         self.randomize_weights()
   
   def randomize_weights(self):
      return

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

   return -1 * params.doubled_pawn_penalty * (white_doubled - black_doubled)


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

   return (wpval + bpval + wkval + bkval + wbval + bbval 
         + wrval + brval + wqval + bqval)

      

def evaluateBoard(board, params):
   if board.is_checkmate():
      if not board.turn:
         return 9999
      else:
         return -9999

   if board.is_game_over():
      return 0

   evaluation = (evaluateMaterial(board, params) 
               + evaluate_doubled_passed_pawns(board, params))

   if board.turn:
      return evaluateMaterial(board, params) 
   else:
      return -1 * evaluateMaterial(board, params)

