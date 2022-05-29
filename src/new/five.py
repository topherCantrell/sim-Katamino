import random

PIECES = [
    {
        '''
        #.
        #.
        #.
        ##
        '''
        'id' : 'A',
        'shape' : '24#.#.#.##', 
        'color' : [244, 117, 33],
    },{
        '''
        ..#
        .##
        ##.
        '''
        'id' : 'B',
        'shape' : '33..#.####.', 
        'color' : [119, 192, 66],
    },{
        '''
        #.#
        ###
        '''
        'id' : 'C',
        'shape' : '32#.####', 
        'color' : [255, 234, 1],
    },
    {
        '''
        #.
        ##
        .#
        .#
        '''
        'id' : 'D',
        'shape' : '24#.##.#.#', 
        'color' : [56, 46, 141],
    },
    {
        'id' : 'E',
        '''
        ###
        .##
        '''
        'shape' : '32###.##', 
        'color' : [208, 108, 170],
    },
    {
        '''
        ..#
        ###
        #..
        '''
        'id' : 'F',
        'shape' : '33..#####..', 
        'color' : [0, 176, 211],
    },
    {
        '''
        #..
        ###
        #..
        '''
        'id' : 'G',
        'shape' : '33#..####..', 
        'color' : [[0, 167, 78]],
    },
    {
        '''
        .#
        ##
        .#
        .#
        '''
        'id' : 'H',
        'shape' : '24.###.#.#', 
        'color' : [113, 55, 31],
    },
    {
        '#####'
        'id' : 'I',
        'shape' : '51#####', 
        'color' : [60, 123, 191],
    },
    {
        '''
        .#.
        ###
        .#.
        '''
        'id' : 'J',
        'shape' : '33.#.###.#.', 
        'color' : [237, 26, 56],
    },
    {
        '''
        ..#
        ###
        .#.
        '''
        'id' : 'K',
        'shape' : '33..####.#.', 
        'color' : [120, 133, 140],
    },{
        '''
        ###
        ..#
        ..#
        '''
        'id' : 'L',
        'shape' : '33###..#..#', 
        'color' : [15, 160, 219],
    },
]

def flip(piece):
    """
    Create a new piece that is flipped along the X axis from the given piece.
    Arguments:
        piece : 2D array -- the ascii representation of the given piece
    Returns:
        2D array -- the ascii representation of the new piece
    """
    # Yes, there is some slice magic I could use here instead
    ret = []
    for y in range(len(piece)-1,-1,-1):
        ret.append(piece[y])
    return ret

def turn(piece,dist):
    """
    Create a new piece that is a clockwise rotation of the given piece.
    The number of turns is passed in, thus "3" is actually 1 rotation
    counterclockwise.
    Arguments:
        piece : 2D array -- the ascii representation of the given piece
    Returns:
        2D array -- the ascii representation of the new piece
    """
    for _ in range(dist):
        ret = []
        for x in range(len(piece[0])):
            nr = []
            for y in range(len(piece)-1,-1,-1):
                nr.append(piece[y][x])
            ret.append(nr)
        piece = ret
    return ret

def print_piece(piece,flat=False):
    """
    Return a string representation of the given piece sutable
    for printing.
    Arguments:    
        piece : 2D array -- the ascii representation of the given piece
        flat: true to leave out line feeds
    Returns:
        string representation of the new piece
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

def shrink(piece):
    """
    Remove the empty columns and rows from a piece
    Arguments:
      piece : the piece to shrink in place
    """
    for y in range(len(piece)-1,-1,-1):
        if not '#' in piece[y]:
            del piece[y]
    for x in range(len(piece[0])-1,-1,-1):
        fnd = False
        for y in range(len(piece)):
            if piece[y][x]=='#':
                fnd = True
                break
        if not fnd:
            for y in range(len(piece)):
                del piece[y][x]

def make_all_pieces():
    uniques = []

    for _ in range(1000):
        piece = [
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],    
        ]

        offs = [
            (0,-1), # Up
            (1,0),  # right
            (0,1),  # down
            (-1,0), # left
        ]

        piece[4][4]='#'
        squares = [(4,4)]

        while(len(squares)<5):
            x,y = random.choice(squares)
            ofx,ofy = random.choice(offs)
            x += ofx
            y += ofy
            if piece[y][x] == '.':
                piece[y][x] = '#'
                squares.append((x,y))

        shrink(piece)
        m_piece = flip(piece)

        if (piece not in uniques and turn(piece,1) not in uniques and turn(piece,2) not in uniques and turn(piece,3) not in uniques and
            m_piece not in uniques and turn(m_piece,1) not in uniques and turn(m_piece,2) not in uniques and turn(m_piece,3) not in uniques):            
            uniques.append(piece)

    return uniques


uniques = make_all_pieces()

for piece in uniques:
    print('-----')
    g = print_piece(piece,flat=True)
    print(g)
    g = print_piece(piece)
    print(g)

print(len(uniques))

# 23#####.
# ##
# ##
# #.

def make_empty_board(num_pieces):
    ret = []
    for y in range(5):
        r = []
        for x in range(num_pieces):
            r.append('.')
        ret.append(r)
    print(ret)
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

board = make_empty_board(4)

piece = uniques[0]
ok,x,y = can_place_piece(board,piece)
if ok:
    place_piece(board,piece,x,y)
print(print_piece(board))

piece = uniques[1]
ok,x,y = can_place_piece(board,piece)
if ok:
    place_piece(board,piece,x,y)
print(print_piece(board))