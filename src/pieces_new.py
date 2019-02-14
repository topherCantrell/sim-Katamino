'''Info about the pieces'''

PIECES = [  # 63 unique (not 12*8 = 96)
    {'id': 1, 'color': [244, 117, 33], 'origin': [0, 3], 'unique': 8,
     'poly': '-5,5 -5,-35 15,-35 15,-25 5,-25 5,5',
     'draws': ['0001', '1112', '2223', '3330', '0003', '1110', '2221', '3332']},
    {'id': 2, 'color': [119, 192, 66], 'origin': [0, 2], 'unique': 4,
     'poly': '-5,5 -5,-5 5,-5 5,-15 15,-15 15,-25 25,-25 25,-5 15,-5 15,5',
     'draws': ['1010', '2121', '3232', '0303', '3030', '0101', '1212', '2323']},
    {'id': 3, 'color': [255, 234, 1], 'origin': [0, 1], 'unique': 4,
     'poly': '-5,5 -5,-15 25,-15 25,5 15,5 15,-5 5,-5 5,5',
     'draws': ['0112', '1223', '2330', '3001', '0332', '1003', '2110', '3221']},

    {'id': 4, 'color': [56, 46, 141], 'origin': [0, 0], 'unique': 8,
     'poly': '-5,5 -5,-5 25,-5 25,5 35,5 35,15 15,15 15,5',
     'draws': ['1121', '2232', '3303', '0010', '3323', '0030', '3233', '0300']},

    {'id': 5, 'color': [208, 108, 170], 'origin': [0, 1], 'unique': 8,
     'draws': ['1103', '2210', '3321', '0032', '3301', '0012', '1123', '2230']},
    {'id': 6, 'color': [0, 176, 211], 'origin': [2, 2], 'unique': 4,
     'draws': ['3003', '0110', '1001', '2112', '1221', '2332', '3223', '0330']},
    {'id': 7, 'color': [0, 167, 78], 'origin': [0, 0], 'unique': 4,
     'draws': ['11322', '22033', '33100', '00211', '33122', '00233', '11300', '22011']},
    {'id': 8, 'color': [113, 55, 31], 'origin': [0, 1], 'unique': 8,
     'draws': ['10211', '21322', '32033', '03100', '30233', '01300', '12011',  '23122']},
    {'id': 9, 'color': [60, 123, 191], 'origin': [0, 0], 'unique': 2,
     'draws': ['1111', '2222', '3333', '0000', '3333', '0000', '1111', '2222']},
    {'id': 10, 'color': [237, 26, 56], 'origin': [1, 0], 'unique': 1,
     'draws': ['220311', '220311', '220311', '220311', '220311', '220311', '220311', '220311']},
    {'id': 11, 'color': [120, 133, 140], 'origin': [0, 0], 'unique': 8,
     'draws': ['30310', '01021', '12132', '23203', '10130', '21201', '32312', '03023']},
    {'id': 12, 'color': [15, 160, 219], 'origin': [0, 1], 'unique': 4,
     'draws': ['1122', '0011', '3300', '2233', '3322', '2211', '1100', '0033', '3323']},
]

_OFS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
_VEC_TRANS = [
    '',
    'rotate(90)',
    'rotate(180)',
    'rotate(270)',
    'matrix(-1 0 0 1 0 0)',
    'matrix(-1 0 0 1 0 0) rotate(270)',
    'matrix(-1 0 0 1 0 0) rotate(180)',
    'matrix(-1 0 0 1 0 0) rotate(90)',
]

for piece in PIECES:
    draw_ofs = []
    for draw in piece['draws']:
        rot = []
        for c in draw:
            rot.append(_OFS[int(c)])
        draw_ofs.append(rot)
    piece['draw'] = draw_ofs


def place_piece(board, piece, x_cor, y_cor, rot):
    '''Place the given piece on the board'''
    good = True
    placed = []
    token = piece['id']
    if board[y_cor][x_cor] != 0 and board[y_cor][x_cor] != token:
        return None
    board[y_cor][x_cor] = token
    placed.append((x_cor, y_cor))
    for drw in piece['draw'][rot]:
        x_cor += drw[0]
        y_cor += drw[1]
        if board[y_cor][x_cor] != 0 and board[y_cor][x_cor] != token:
            good = False
            break
        board[y_cor][x_cor] = token
        placed.append((x_cor, y_cor))
    if good:
        return placed
    for rem in placed:
        board[rem[1]][rem[0]] = 0
    return None


_SVG_ELEMENT = ''' 
    <g transform="translate({x},{y}) {trans} scale({scale})" style="fill:rgb({cr},{cg},{cb});stroke-width:.05;stroke:#000">
        <polygon points="{points}">
    </g>'''


def get_svg(piece, x_cor, y_cor, rot=0, scale=1):
    element = _SVG_ELEMENT.format(x=x_cor, y=y_cor, trans=_VEC_TRANS[rot], scale=scale,
                                  cr=piece['color'][0], cg=piece['color'][1], cb=piece['color'][2],
                                  points=piece['poly'])
    return element


import board_new
piece = PIECES[3]

b = board_new.new_board(500, 50)

for i in range(8):
    s = get_svg(piece, 50 + 50 * i, 50, i)
    place_piece(b, piece, 10 * i, 20, i)
    print(s)

br = board_new.get_string_rep(b)
br = board_new.strip_string_rep(br)
print(br)
