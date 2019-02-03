import random
import board

b = board.new_board(20,20)

cells = [(10,10)]

b[10][10] = 'X'

for _ in range(4):
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
board.print_board(nb)