'''All things board

 1   5  1,5                            1x5
 2  10  1,2,5,10                       1x10, 2x5
 3  15  1,3,5,15                       1x15, 3x5 
 4  20  1,2,4,5,10,20                  1x20, 2x10, 4x5 
 5  25  1,5,25                         1x25, 5x5
 6  30  1,2,3,5,6,10,15,30             1x30, 2x15, 3x10, 6x5
 7  35  1,5,7,35                       1x35, 7x5 
 8  40  1,2,4,5,8,10,20,40             1x40, 2x20, 4x10, 8x5 
 9  45  1,3,5,9,15,45                  1x45, 3x15, 9x5 
10  50  1,2,5,10,25,50                 1x50, 2x25, 10x5
11  55  1,5,11,55                      1x55, 11x5
12  60  1,2,3,4,5,6,10,12,15,20,30,60  1x60, 3x20, 2x30, 4x15, 12x5, 6x10

'''

BOARDS_FOR_PIECES = [
    [ ],
    [ [1,5] ],
    [ [2,5], [1,10] ],
    [ [3,5], [1,15] ],
    [ [4,5], [1,20], [2,10] ],
    [ [5,5], [1,25] ],
    [ [6,5], [1,30], [2,15], [3,10] ],
    [ [7,5], [1,35] ],
    [ [1,40], [2,20], [4,10] ], # [8,5],
    [ [9,5], [1,45], [3,15] ],
    [ [10,5],[1,50], [2,25] ],
    [ [11,5],[1,55] ],
    [ [12,5],[1,60], [3,20], [2,30],[4,15],[6,10] ],
]


def new_board(width, height=5):
    '''Create a new board'''
    ret = []
    for _ in range(height):
        ret.append([0] * width)
    return ret


def get_string_rep(board):
    '''Make a string representation of the board'''
    ret = ''
    for row in board:
        for ch_token in row:
            if ch_token == 0:
                ret = ret + '.'
            else:
                if ch_token < 0:
                    ch_token = -ch_token
                    ret = ret + chr(ch_token + 96)
                else:
                    ret = ret + chr(ch_token + 64)
        ret = ret + '\n'
    return ret.strip()


def strip_string_rep(brd):
    '''Remove the space around the center of a board representation (not a board)'''
    b = brd.split('\n')
    li = len(b[0])
    lj = 0
    blank = '.' * len(b[0])
    for i in range(len(b) - 1, -1, -1):
        if b[i] == blank:
            del b[i]
            continue
        g = b[i]
        ki = 0
        while g[ki] == '.':
            ki = ki + 1
        kj = len(g) - 1
        while g[kj] == '.':
            kj = kj - 1
        if ki < li:
            li = ki
        if kj > lj:
            lj = kj
    for i in range(len(b)):
        g = b[i][li:lj + 1]
        b[i] = g
    return '\n'.join(b)


def rotate_cw(board):
    ret = []
    for x in range(len(board[0])):
        r = ''
        for y in range(len(board) - 1, -1, -1):
            r = r + board[y][x]
        ret.append(r)
    return ret


def flip_top_bottom(board):
    ret = []
    for b in board:
        ret.insert(0, b)
    return ret


def flip_left_right(board):
    ret = []
    for b in board:
        ret.append(b[::-1])
    return ret
