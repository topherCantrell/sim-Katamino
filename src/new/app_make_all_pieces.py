import random

import pieces

import boards

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
        m_piece = pieces.flip(piece)

        if (piece not in uniques and pieces.turn(piece,1) not in uniques and pieces.turn(piece,2) not in uniques and pieces.turn(piece,3) not in uniques and
            m_piece not in uniques and pieces.turn(m_piece,1) not in uniques and pieces.turn(m_piece,2) not in uniques and pieces.turn(m_piece,3) not in uniques):            
            uniques.append(piece)

    return uniques

uniques = make_all_pieces()

for piece in uniques:
    print('-----')
    g = boards.print_board(piece,flat=True)
    print(g)
    g = boards.print_board(piece)
    print(g)

print(len(uniques))
