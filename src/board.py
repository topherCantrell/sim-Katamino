"""
Board functions: rotating, printing, etc.
"""

def new_board(width, height=5):
    """Make a new (empty) board"""
    board = []
    for _ in range(0, height):
        row = []
        for _ in range(0, width):
            row.append('.')
        board.append(row)
    return board


def write_board(board, out):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            out.write(col)
        out.write('\n')
    out.write('\n')


def print_board(board):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            print(col, end='')
        print()
    print()


def strip_board(b):
    li = len(b[0])
    lj = 0
    blank = ['.'] * len(b[0])
    for i in range(len(b)-1,-1,-1):
        if b[i]==blank:
            del b[i]
            continue
        g = b[i]
        ki = 0
        while g[ki]=='.':
            ki = ki + 1
        kj = len(g)-1
        while g[kj]=='.':
            kj = kj - 1
        if ki<li:
            li = ki
        if kj>lj:
            lj = kj
    for i in range(len(b)):
        g = b[i][li:lj+1]
        b[i] = g       

def rotate_cw(board):
    ret = []
    for x in range(len(board[0])):
        r = ''
        for y in range(len(board)-1,-1,-1):
            r = r + board[y][x]
        ret.append(r)
    return ret            
              
  
def flip_top_bottom(board):
    ret = []
    for b in board:
        ret.insert(0,b)
    return ret

def flip_left_right(board):
    ret = []
    for b in board:
        ret.append(''.join(reversed(b)))
    return ret
