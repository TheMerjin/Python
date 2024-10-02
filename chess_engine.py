import copy as c
class Piece:
    none = 0
    king = 1
    pawn = 2
    knight = 3
    bishop = 4
    rook = 5
    queen = 6

    white = 8
    black = 16
    def __init__(self,piece_type, color):
        self.piece_type = piece_type
        self.color = color
class GameState():
    def __init__(self):
        #Board representation 8*8 list 2 dimensional. Each element is an instance of piece object the piece and color are 
        self.board = [
            [Piece(Piece.rook, Piece.black),Piece(Piece.knight, Piece.black),Piece(Piece.bishop, Piece.black),Piece(Piece.queen, Piece.black),Piece(Piece.king, Piece.black),Piece(Piece.bishop, Piece.black),Piece(Piece.knight, Piece.black),Piece(Piece.rook, Piece.black)],
            [Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black),Piece(Piece.pawn, Piece.black)],
            [Piece(Piece.none, None), Piece(Piece.none, None), Piece(Piece.none,  None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None)],
            [Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None)],
            [Piece(Piece.none, None) ,Piece(Piece.none, None) ,Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none,None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None)],
            [Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None),Piece(Piece.none, None)],
            [Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white),Piece(Piece.pawn, Piece.white)],
            [Piece(Piece.rook, Piece.white),Piece(Piece.knight, Piece.white),Piece(Piece.bishop, Piece.white),Piece(Piece.queen, Piece.white),Piece(Piece.king, Piece.white),Piece(Piece.bishop, Piece.white),Piece(Piece.knight, Piece.white),Piece(Piece.rook, Piece.white)]]
        self.white_to_move = True
        self.move_log = []
        self.white_king_pos = (4,7)
        self.black_king_pos = (4,0)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = Piece(Piece.none, None)
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved.piece_type == 1:
            if move.piece_moved.color == 8:
                self.white_king_pos = (move.start_col, move.end_col)
            elif move.piece_moved.color == 16:
                self.black_king_pos = (move.start_col, move.end_col)
            
        
    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # swap players
            
    def get_legal_moves(self):
        valid_moves = c.copy(self.get_psuedolegal_moves())
        for n in range(len(valid_moves)-1,-1,-1):
            self.make_move(valid_moves[n])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                print(f'removed move {valid_moves[n].moveId}')
                valid_moves.remove(valid_moves[n])
            self.white_to_move = not self.white_to_move
            self.undoMove()

        return valid_moves
    


    def square_under_attack(self,col,row):
        """
        if enemy can attack a certain square
        """
        self.white_to_move = not self.white_to_move
        The_opponent_reponses_that_they_can_possibly_play = self.get_psuedolegal_moves()
        for opp_move in The_opponent_reponses_that_they_can_possibly_play:
            print(f'possible opponent responses {opp_move.moveId} and length {len(The_opponent_reponses_that_they_can_possibly_play)}')
        #1+1 = 2
        self.white_to_move = not self.white_to_move
        for opp_move in The_opponent_reponses_that_they_can_possibly_play:
            if opp_move.end_row == row and opp_move.end_col ==col:
                print(f'move to delete{opp_move.moveId}')
                return True
        return False
    def in_check(self):
        """
        deterine if player in check
        
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_pos[0], self.white_king_pos[1])
        if not self.white_to_move:
            return self.square_under_attack(self.black_king_pos[0], self.black_king_pos[1]) 
    def get_psuedolegal_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row][col]
                if self.white_to_move and piece.color == 8:
                    if piece.piece_type == 2: # is piece is a pawn
                        self.getpawnmoves(row,col,moves)
                    if piece.piece_type == 1 : #if piece is a King
                        self.getkingmoves(row,col,moves)
                    if piece.piece_type == 3:# is piece is a knight
                        self.getknightmoves(row,col,moves)
                    if piece.piece_type == 4:# is piece is a bishop
                        self.getbishopmoves(row, col, moves)
                    if piece.piece_type == 5: #rook is a piece
                        self.getrookmoves(row, col, moves)
                    if piece.piece_type == 6: # if the piece is a Queen 
                        self.getqueenmoves(row, col, moves)

                elif self.white_to_move == False and piece.color == 16:
                    if piece.piece_type == 2:# is piece is a pawn
                        self.getpawnmoves(row,col,moves)
                    if piece.piece_type == 1 : #if piece is a King
                        self.getpawnmoves(row,col,moves)
                    if piece.piece_type == 3:# is piece is a knight
                        self.getknightmoves(row,col,moves)
                    if piece.piece_type == 4:# is piece is a bishop
                        self.getbishopmoves(row,col,moves)
                    if piece.piece_type == 5: #rook is a piece
                        self.getrookmoves(row,col,moves)
                    if piece.piece_type == 6: # if the piece is a Queen 
                        self.getqueenmoves(row,col,moves)
        return moves
    def getpawnmoves(self,row,col,moves):
        if self.white_to_move:
            if self.board[row-1][col].piece_type == Piece.none:
                new_move  = Move((col,row),(col,row-1), self.board)
                moves.append(new_move)
                if row == 6:
                    if self.board[row-2][col].piece_type == Piece.none:
                        new_double_move = Move((col,row), (col,row-2), self.board)
                        moves.append(new_double_move)
            if col <= 6:
                if self.board[row-1][col+1].color == Piece.black:
                    capture_right = Move((col,row),(col+1, row-1), self.board)
                    moves.append(capture_right)
            if col >=1:
                if self.board[row-1][col-1].color == Piece.black:
                    capture_left = Move((col,row),(col-1, row-1), self.board)  
                    moves.append(capture_left)
                

        if not self.white_to_move:
            if self.board[row+1][col].piece_type == Piece.none:
                moves.append(Move((col,row),(col,row+1), self.board))
                if row == 1:
                    if self.board[row+2][col].piece_type == Piece.none:
                        new_double_move = Move((col,row), (col,row+2), self.board)
                        moves.append(new_double_move)
            if col <= 6:
                if self.board[row+1][col+1].color == Piece.white:
                    capture_left = Move((col,row),(col+1, row+1), self.board)
                    moves.append(capture_left)
            if col >=1:
                if self.board[row+1][col-1].color == Piece.white:
                    capture_right = Move((col,row),(col-1, row+1), self.board)  
                    moves.append(capture_right)



    


    def getkingmoves(self, row, col, moves):
        if self.white_to_move:
            if (row+1) <= 7:
                target_square = self.board[row+1][col]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col, row+1), self.board)
                    moves.append(new_move)

            if (col + 1 )<=7:
                target_square = self.board[row][col+1]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col+1,row), self.board)
                    moves.append(new_move)
            if (row-1) >=0:
                target_square = self.board[row-1][col]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col, row-1), self.board)
                    moves.append(new_move)
            if (col-1) >= 0:
                target_square = self.board[row][col-1]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col-1, row), self.board)
                    moves.append(new_move)
            if (row-1)>=0 and (col-1)>=0:
                target_square = self.board[row-1][col-1]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col-1, row-1), self.board)
                    moves.append(new_move)
            if (row-1)>=0 and (col+1)<=7:
                target_square = self.board[row-1][col+1]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col+1, row-1), self.board)
                    moves.append(new_move)
            if (row+1) <=7 and (col-1)>=0:
                target_square = self.board[row+1][col-1]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col-1, row+1), self.board)
                    moves.append(new_move)
            if (row+1)<=7 and (col+1) <=7:
                target_square = self.board[row+1][col+1]
                if target_square.color == Piece.white:
                    pass
                else:
                    new_move = Move((col,row), (col+1, row+1), self.board)
                    moves.append(new_move)
        if not self.white_to_move:
            if (row+1) <= 7:
                target_square = self.board[row+1][col]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col, row+1), self.board)
                    moves.append(new_move)

            if (col + 1 )<=7:
                target_square = self.board[row][col+1]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col+1,row), self.board)
                    moves.append(new_move)
            if (row-1) >=0:
                target_square = self.board[row-1][col]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col, row-1), self.board)
            if (col-1) >= 0:
                target_square = self.board[row][col-1]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col-1, row), self.board)
                    moves.append(new_move)
            if (row-1)>=0 and (col-1)>=0:
                target_square = self.board[row-1][col-1]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col-1, row-1), self.board)
                    
                    moves.append(new_move)
            if (row-1)>=0 and (col+1)<=7:
                target_square = self.board[row-1][col+1]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col+1, row-1), self.board)
                    moves.append(new_move)
            if (row+1) <=7 and (col-1)>=0:
                target_square = self.board[row+1][col-1]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col-1, row+1), self.board)
                    
                    moves.append(new_move)
            if (row+1)<=7 and (col+1) <=7:
                target_square = self.board[row+1][col+1]
                if target_square.color == Piece.black:
                    pass
                else:
                    new_move = Move((col,row), (col+1, row+1), self.board)
                    
                    moves.append(new_move)

        

            
            
        



    def getknightmoves(self, row, col, moves):
        if self.white_to_move:
            possible_offsets = [(1,2),(2,1), (-1,2), (-2,1), (-1,-2), (-2,-1), (1,-2), (2,-1)]
            for x,y in possible_offsets:
                target_row = row + y
                target_col = col + x
                if target_row > -1 and target_row < 8 and target_col > -1 and target_col < 8 :
                    target_square = self.board[target_row][target_col]
                    if target_square.color == Piece.white:
                        pass
                    else:
                        new_knight_move = Move((col,row), (target_col, target_row), self.board)
                        moves.append(new_knight_move)
        if not self.white_to_move:
            possible_offsets = [(1,2),(2,1), (-1,2), (-2,1), (-1,-2), (-2,-1), (1,-2), (2,-1)]
            for x,y in possible_offsets:
                target_row = row + y
                target_col = col + x
                if target_row > -1 and target_row < 8 and target_col > -1 and target_col < 8 :
                    target_square = self.board[target_row][target_col]
                    if target_square.color == Piece.black:
                        pass
                    else:
                        new_knight_move = Move((col,row), (target_col, target_row), self.board)
                        moves.append(new_knight_move)
            
    def getbishopmoves(self, row, col, moves):
        if self.white_to_move:
        # Move diagonally top-left
            for n in range(1, min(row + 1, col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row - n][col - n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col - n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col - n, row - n), self.board))
            for n in range(1, min(7 - row + 1, 7- col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row + n][col + n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
            for n in range(1, min(row+1, 7 -col + 1)):
                target_square = self.board[row-n][col+n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
            for n in range(1, min(7- row + 1 , col + 1)):
                target_square = self.board[row+n][col-n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))


                


        if not self.white_to_move:
            for n in range(1, min(row + 1, col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row - n][col - n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col - n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col - n, row - n), self.board))
            for n in range(1, min(7 - row + 1, 7- col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row + n][col + n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
            for n in range(1, min(row+1, 7 -col + 1)):
                target_square = self.board[row-n][col+n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
            for n in range(1, min(7- row + 1 , col + 1)):
                target_square = self.board[row+n][col-n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))

    
    def getrookmoves(self, row, col, moves):
        if self.white_to_move:
        # Find possible upward moves
            for n in range(1, row + 1):  # Start from 1 to row (inclusive)
                target_square = self.board[row - n][col]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
            for n in range(1,(7-row)+1):
                target_square = self.board[row+n][col]
                if target_square.color == Piece.white:
                    break
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
            for n in range(1,col+1):
                target_square = self.board[row][col-n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
            for n in range(1,(7-col)+1):
                target_square = self.board[row][col+n]
                if target_square.color == Piece.white:
                    break
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
        if not self.white_to_move:
            for n in range(1, row + 1):  # Start from 1 to row (inclusive)
                target_square = self.board[row - n][col]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
            for n in range(1,(7-row)+1):
                target_square = self.board[row+n][col]
                if target_square.color == Piece.black:
                    break
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
            for n in range(1,col+1):
                target_square = self.board[row][col-n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
            for n in range(1,(7-col)+1):
                target_square = self.board[row][col+n]
                if target_square.color == Piece.black:
                    break
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
            
            

              
        
                  

        
              
        


    def getqueenmoves(self, row, col, moves):
        if self.white_to_move:
            for n in range(1, row + 1):  # Start from 1 to row (inclusive)
                target_square = self.board[row - n][col]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
            for n in range(1,(7-row)+1):
                target_square = self.board[row+n][col]
                if target_square.color == Piece.white:
                    break
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
            for n in range(1,col+1):
                target_square = self.board[row][col-n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
            for n in range(1,(7-col)+1):
                target_square = self.board[row][col+n]
                if target_square.color == Piece.white:
                    break
                elif target_square.color == Piece.black:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
                for n in range(1, min(row + 1, col + 1)):  # Ensure we stay within board limits
                    target_square = self.board[row - n][col - n]
                    if target_square.color == Piece.white:
                        break  # Stop if a friendly piece is encountered
                    elif target_square.color == Piece.black:
                        moves.append(Move((col, row), (col - n, row - n), self.board))
                        break
                    else:
                        moves.append(Move((col, row), (col - n, row - n), self.board))
            for n in range(1, min(7 - row + 1, 7- col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row + n][col + n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
            for n in range(1, min(row+1, 7 -col + 1)):
                target_square = self.board[row-n][col+n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
            for n in range(1, min(7- row + 1 , col + 1)):
                target_square = self.board[row+n][col-n]
                if target_square.color == Piece.white:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.black:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))

        if not self.white_to_move:
            for n in range(1, row + 1):  # Start from 1 to row (inclusive)
                target_square = self.board[row - n][col]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row - n), self.board)
                    moves.append(new_move)
            for n in range(1,(7-row)+1):
                target_square = self.board[row+n][col]
                if target_square.color == Piece.black:
                    break
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col, row+n ), self.board)
                    moves.append(new_move)
            for n in range(1,col+1):
                target_square = self.board[row][col-n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col-n, row), self.board)
                    moves.append(new_move)
            for n in range(1,(7-col)+1):
                target_square = self.board[row][col+n]
                if target_square.color == Piece.black:
                    break
                elif target_square.color == Piece.white:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
                    break
                else:
                    new_move = Move((col, row), (col+n,row), self.board)
                    moves.append(new_move)
            for n in range(1, min(row + 1, col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row - n][col - n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col - n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col - n, row - n), self.board))
            for n in range(1, min(7 - row + 1, 7- col + 1)):  # Ensure we stay within board limits
                target_square = self.board[row + n][col + n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row + n), self.board))
            for n in range(1, min(row+1, 7 -col + 1)):
                target_square = self.board[row-n][col+n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col +  n, row - n), self.board))
            for n in range(1, min(7- row + 1 , col + 1)):
                target_square = self.board[row+n][col-n]
                if target_square.color == Piece.black:
                    break  # Stop if a friendly piece is encountered
                elif target_square.color == Piece.white:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))
                    break
                else:
                    moves.append(Move((col, row), (col -  n, row + n), self.board))
            
            


class Move():
    def __init__(self,sq_start, sq_end, board):
        self.start_col = sq_start[0]
        self.start_row = sq_start[1]
        self.end_col = sq_end[0]
        self.end_row = sq_end[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveId = self.start_row*100+self.start_col*1000 + self.end_row*1+self.end_col*10

        
    '''
    We must overide an equals method here.
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        else:
            return False