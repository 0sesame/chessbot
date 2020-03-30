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
      self.rook_hor_mobility = 5
      self.rook_vert_mobility = 20
      
      if randomize == True:
         self.randomize_weights()
   
   def randomize_weights(self):
      return

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

   return (params.rook_hor_mobility*(white_hor_mobility - black_hor_mobility) +
           params.rook_vert_mobility*(white_vert_mobility - black_vert_mobility))
         
   
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
               + evaluate_doubled_passed_pawns(board, params)
               + evaluate_rook_mobility(board, params))

   if board.turn:
      return evaluateMaterial(board, params) 
   else:
      return -1 * evaluateMaterial(board, params)

