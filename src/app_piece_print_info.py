import board_utils
import piece_utils

for piece in piece_utils.PIECES:
    print(piece['id'], end='')
    min_wid_ind = -1
    min_wid = 50
    for i in range(8):
        board = board_utils.new_board(20, 20)
        piece_utils.place_piece(board, piece, 10, 10, i)
        br = board_utils.get_string_rep(board)
        br = board_utils.strip_string_rep(br).split('\n')
        width = len(br[0])
        height = len(br)
        if width < min_wid:
            min_wid = width
            min_wid_ind = i
        yy = -1
        xx = -1
        for y in range(height):
            for x in range(width):
                if br[y][x] != '.' and br[y][x] == br[y][x].lower():
                    yy = y
                    xx = x
                    break
        # print(br)
        print('[{},{},{},{}],'.format(xx, yy, width, height), end='')
    print(min_wid_ind)

'''
b = board_utils.new_board(500, 50)

for i in range(8):
    s = get_svg(piece, 50 + 50 * i, 50, i)
    place_piece(b, piece, 50 + 10 * i, 20, i)
    print(s)

br = board_utils.get_string_rep(b)
br = board_utils.strip_string_rep(br)
print(br)


for piece in PIECES:
    print(piece['id'])
    uniq = []
    for i in range(8):
        b = board_utils.new_board(20, 20)
        place_piece(b, piece, 10, 10, i)
        br = board_utils.get_string_rep(b)
        br = board_utils.strip_string_rep(br)
        br = br.upper()
        if br in uniq:
            print('Rotation', i, 'is redundant')
        else:
            uniq.append(br)
'''
