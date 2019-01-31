import cull
import pieces

CELL_SIZE = 10


def make_board(board, f, n):

    f.write('<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'.format(
        width=1000, height=CELL_SIZE * 5))
    for y in range(5):
        for x in range(len(board[0])):
            c = board[y][x]
            piece = pieces.get_piece_by_name(c)
            color = piece.color
            f.write('<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:rgb({r},{g},{b})"/>\n'.format(
                x=x * CELL_SIZE + n, y=y * CELL_SIZE, width=CELL_SIZE, height=CELL_SIZE, r=color[0], g=color[1], b=color[2]))

    f.write('</svg>\n')


solutions = cull.get_unique_solutions('../smallSlamRAW.txt')

f = None
current_num = None
for solution in solutions:
    i = solution[0].index(':')
    sn = solution[0][0:i]
    if sn != current_num:
        current_num = sn
        if f:
            f.close()
        f = open('../art/smallSlam-' + sn + '.svg', 'w')
    for i in range(len(solution[1])):
        make_board(solution[1][i], f, (5 * CELL_SIZE + 2) * i)
