def make_empty_board(num_pieces):
    ret = []
    for y in range(5):
        r = []
        for x in range(num_pieces):
            r.append('.')
        ret.append(r)
    #print(ret)
    return ret

def place_piece(board,piece,x,y):
    for iy in range(len(piece)):
        for ix in range(len(piece[0])):
            a = piece[iy][ix]
            if a=='.':
                continue
            if board[y+iy][x+ix]!='.':
                raise Exception('Space not empty')
            board[y+iy][x+ix] = piece[iy][ix]

def can_place_piece_at(board,piece,x,y):    
    for iy in range(len(piece)):                
        for ix in range(len(piece[0])):
            a = board[y+iy][x+ix]
            b = piece[iy][ix]
            if b=='.' or a=='.':
                continue
            return False
    return True

def can_place_piece(board,piece):
    for y in range(len(board)-len(piece)+1):
        for x in range(len(board[0])-len(piece[0])+1):
            ok = True
            for iy in range(len(piece)):                
                for ix in range(len(piece[0])):
                    a = board[y+iy][x+ix]
                    b = piece[iy][ix]
                    if b=='.' or a=='.':
                        continue
                    ok = False
                    break
                if not ok:
                    break 
            if ok:
                break
        if ok:
            break       
    return ok,x,y

def print_board(piece,flat=False):
    """
    Return a string representation of the given board (or piece) suitable
    for printing.
    Arguments:    
        piece : 2D array -- the ascii representation of the given board
        flat: true to leave out line feeds
    Returns:
        string representation of the board
    """
    ret = ''
    if flat:
        ret = str(len(piece[0]))+str(len(piece))
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            ret = ret + piece[y][x]
        if not flat:
            ret = ret + '\n'
    return ret