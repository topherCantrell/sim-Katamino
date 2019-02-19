'''All things board'''


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
