def new_board(width, height=5):
    ret = []
    for _ in range(height):
        ret.append([0] * width)
    return ret


def get_string_rep(board):
    ret = ''
    for row in board:
        for c in row:
            if c == 0:
                ret = ret + '.'
            else:
                ret = ret + chr(c + 64)
        ret = ret + '\n'
    return ret.strip()


def strip_string_rep(br):
    b = br.split('\n')
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
