import cull
import pieces

CELL_SIZE = 10


def make_board(board, f, xo, yo):

    for y in range(5):
        for x in range(len(board[0])):
            c = board[y][x]
            piece = pieces.get_piece_by_name(c)
            color = piece.color
            f.write('<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:rgb({r},{g},{b})"/>\n'.format(
                x=xo + x * CELL_SIZE, y=yo + y * CELL_SIZE, width=CELL_SIZE, height=CELL_SIZE, r=color[0], g=color[1], b=color[2]))


solutions = cull.get_unique_solutions('../smallSlamRAW.txt')

for solution in solutions:

    i = solution[0].index(':')
    sn = solution[0][0:i]
    fn = 'small-' + sn + '-' + solution[0][i + 1:].strip() + '.svg'

    # TODO calculate width and height

    print(solution[0] + '<br>')
    print('![](art/' + fn + ')<br>')
    with open('../art/' + fn, 'w') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n'.format(
            width=1000, height=CELL_SIZE * 5))
        xo = 0
        yo = 0
        for i in range(len(solution[1])):
            make_board(solution[1][i], f, xo, yo)
            xo = xo + len(solution[1][i][0]) * CELL_SIZE + 8
            # TODO CR after so many

        f.write('</svg>\n')
