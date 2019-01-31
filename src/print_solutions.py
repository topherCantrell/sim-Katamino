import cull
import pieces

CELL_SIZE = 10

def make_board(board):
    
    print('<svg width="{width}" height="{height}">'.format(width=len(board[0])*CELL_SIZE, height=CELL_SIZE*5))
    for y in range(5):
        for x in range(len(board[0])):
            c = board[y][x]    
            piece = pieces.get_piece_by_name(c)
            color = piece.color
            print('<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:rgb({r},{g},{b})"/>'.format(
                x=x*CELL_SIZE,y=y*CELL_SIZE,width=CELL_SIZE,height=CELL_SIZE,r=color[0],g=color[1],b=color[2]))
    
    print('</svg>')

solutions = cull.get_unique_solutions('../smallSlamRAW.txt')

for solution in solutions:
    print('<br>'+solution[0]+'<br>')
    for board in solution[1]:
        make_board(board)

