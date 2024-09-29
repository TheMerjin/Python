import pygame as p
import chess_engine as c
p.init()
width = height = 640
board_length = 8
board_dimension = 8*8
sq_size = height // board_length
fps = 15
# access images
images = {}


def image_load():
    all_pieces = ['wP', 'wB', 'wR', 'wK', 'wN', 'wQ', 
                  'bP', 'bB', 'bR', 'bN', 'bQ', 'bK']
    
    for piece in all_pieces:
        images[piece] = p.transform.scale(
            p.image.load(f'C:\\Users\\Sreek\\OneDrive\\Desktop\\Python\\images\\{piece}.png'),
            (sq_size, sq_size)
        )
image_load()




def main():   
    screen = p.display.set_mode((width, height))
    screen.fill(p.Color("white"))
    image_load()
    gs = c.GameState()
    
    valid_moves = gs.get_psuedolegal_moves()
    print(valid_moves)
    move_made = False
    sq_selected = () #Tuple(x,y)
    piece_selected = c.Piece(c.Piece.none, None)
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                exit()
                running = False
            if e.type == p.KEYDOWN:
                gs.undoMove()
                print(f'Move Log is here : {gs.move_log}')
            if e.type == p.MOUSEBUTTONDOWN:
                location =  p.mouse.get_pos()
                col = location[0]//sq_size
                row = location[1]//sq_size
                piece_selected = gs.board[row][col]
                if piece_selected.color is not None:
                    sq_selected = (col,row)
                
                    
                
            if e.type == p.MOUSEBUTTONUP:
                new_location = p.mouse.get_pos()
                new_col = new_location[0]//sq_size
                new_row = new_location[1]//sq_size
                final_square = (new_col, new_row)
                final_selected = gs.board[row][col]


                if piece_selected:
                    if piece_selected:
                        
                        move = c.Move(sq_selected,final_square,gs.board)
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                        piece_selected = c.Piece(c.Piece.none, None)
            if move_made:
                valid_moves = gs.get_psuedolegal_moves()
            if piece_selected: 
                if piece_selected.piece_type != 0:
                    location = p.mouse.get_pos()
                    screen.fill(p.Color("white"))  # Clear the screen
                    draw_board_and_game_state(screen, gs)  # Redraw the board and pieces
                    piece_image = f"{'w' if piece_selected.color == c.Piece.white else 'b'}" + \
                                  {2: 'P', 3: 'N', 4: 'B', 5: 'R', 6: 'Q', 1: 'K'}[piece_selected.piece_type]
                    screen.blit(images[piece_image], (location[0] - sq_size // 2, location[1] - sq_size // 2))
                    p.display.flip()

                


        draw_board_and_game_state(screen, gs)
        p.display.flip()


def draw_board_and_game_state(screen, gs):
    draw_checkerboard(screen)
    draw_pieces(screen,gs.board)
    

def draw_checkerboard(screen):
    colors = [p.Color("white"), p.Color("green")]  # Define your colors
    for row in range(board_length):
        for col in range(board_length):
            color = colors[(row + col) % 2]  # Alternate colors
            p.draw.rect(screen, color, p.Rect(col * sq_size, row * sq_size, sq_size, sq_size))
def draw_pieces(screen, board):
    for row in range(board_length):
        for col in range(board_length):
            piece = board[row][col]
            if piece.color is not None:
                piece_image = f"{'w' if piece.color == c.Piece.white else 'b'}" + \
                              {2: 'P', 3: 'N', 4: 'B', 5: 'R', 6: 'Q', 1: 'K'}[piece.piece_type]
                screen.blit(images[piece_image], p.Rect(col * sq_size, row * sq_size, sq_size, sq_size))

    

main()
#How do we figure out the legal moves
#loop over each piece figuring legal moves for each piece
