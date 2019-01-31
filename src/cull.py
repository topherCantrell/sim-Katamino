
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

with open('../smallSlamRAW.txt') as f:
    lines = f.readlines()
    
times = {}

pos = 0
while not lines[pos].startswith('----'):
    g = lines[pos].strip()
    pos += 1
    if ':' in g:
        i = g.index('.')
        j = g.rindex('.')
        n = g[0:i]
        ti = g[j+1:]
        if ti=='0':
            ti = '<1'
        times[n] = ti
    
solutions = []
pos += 1

current = None

while pos<len(lines):
    g = lines[pos]
    pos += 1
    g = g.strip()
    if not g:
        continue
    if ':' in g:
        #print(g + ' ' +times[g])
        current = []
        solutions.append([g,current])
    else:        
        board = []
        board.append(g)
        for _ in range(4):
            board.append(lines[pos].strip())
            pos += 1
        if board in current:
            continue
        if flip_left_right(board) in current:
            continue
        if flip_top_bottom(board) in current:
            continue
        if flip_top_bottom(flip_left_right(board)) in current:
            continue
        current.append(board)
        #print(board)
        
print(solutions)        