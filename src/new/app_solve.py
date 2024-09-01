
import boards
import pieces
import copy

pieces.init()

pieces_set = [
    pieces.get_piece('A'),
    pieces.get_piece('H'),
    pieces.get_piece('G'),
    pieces.get_piece('E'),
    pieces.get_piece('B'),
    pieces.get_piece('F'),
    pieces.get_piece('L'),
    pieces.get_piece('D'),
]
board = boards.make_empty_board(len(pieces_set))

def place_pieces(board,pieces,solutions):

    #print('placing',len(pieces))
        
    my_piece = pieces[0]    
    rotates = my_piece['rotates']

    for rot in range(len(rotates)):
        pt = rotates[rot]
        scroll_width = len(board[0]) - len(pt[0]) # Piece won't fit after this
        scroll_height = len(board) - len(pt) # Or after this          

        for y in range(scroll_height+1):
            for x in range(scroll_width+1):
                if boards.can_place_piece_at(board,pt,x,y):
                    nb = copy.deepcopy(board)
                    boards.place_piece(nb,pt,x,y)   
                    np =  pieces[1:]               
                    #print(boards.print_board(nb))
                    if np:
                        place_pieces(nb,np,solutions)
                    else:
                        # TODO add to solutions                        
                        print(boards.print_board(nb))
                        print()


place_pieces(board,pieces_set,None)

    