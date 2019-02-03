import random
import board

def one_piece(num):
    x = int(num*3/2)
    b = board.new_board(num*3,num*3)
    
    cells = [(x,x)]
    
    b[x][x] = 'X'
    
    for _ in range(num-1):
        while True:
            c = random.choice(cells)
            x = c[0]
            y = c[1]
            s = random.randint(0,3)
            if s==0:
                y = y - 1
            elif s==1:
                y = y + 1
            elif s==2:
                x = x - 1
            else:
                x = x + 1
            if b[y][x]=='.':
                break
        cells.append((x,y))
        b[y][x] = 'X'
                
    nb = []
    for s in b:
        row = ''
        for c in s:
            row = row + c
        nb.append(row)
        
    board.strip_board(nb)
    
    return nb

''' 

TLR
000 none
001 rotate
010 left_right
011 left_right, rotate
100 top_bottom
101 top_bottom, rotate
110 top_bottom, left_right
111 top_bottom, left_right, rotate

''' 


# 1 has 1 2d combination
# 2 has 1 2d combination
# 3 has 2 2d combinations
# 4 has 5 2d combinations
# 5 has 12 2d combinations
# 6 has 35 2d combinations
# 7 has 108 2d combinations

brds = []
for _ in range(80000):
    b = one_piece(7)
    if b in brds: 
        continue # 000    
    if board.rotate_cw(b) in brds:
        continue # 001
    if board.flip_left_right(b) in brds: 
        continue # 010
    if board.flip_left_right(board.rotate_cw(b)) in brds:
        continue # 011
    if board.flip_top_bottom(b) in brds:
        continue # 100    
    if board.flip_top_bottom(board.rotate_cw(b)) in brds:
        continue # 101
    if board.flip_top_bottom(board.flip_left_right(b)) in brds:
        continue # 110
    if board.flip_top_bottom(board.flip_left_right(board.rotate_cw(b))) in brds:
        continue # 111    
    brds.append(b)
    
for g in brds:
    board.print_board(g)
    
print(len(brds))


'''

X.  D
X.
XX
.X

X.. L
X..
XXX

.X E
XX
XX

.XX F
.X.
XX.

XX. K
.XX
.X.

.X. J
XXX
.X.

.X H
XX
.X
.X

XXX G
.X.
.X.

XX. B
.XX
..X

XX C
X.
XX

XX A
.X
.X
.X

XXXXX I

'''