
class Piece:

    def __init__(self, name, draw_spec, color, print_ofs=[0, 0], polygon=''):
        self.name = name
        self.draw_spec = draw_spec
        self.color = color
        self.draws = []
        self.print_ofs = print_ofs
        self.polygon = polygon
        for rot in range(8):
            draw = []
            self.draws.append(draw)
            for dir_char in draw_spec.upper():
                draw.append(_ROTS[rot][dir_char])

    def can_place(self, board, x_start, y_start, rotation):
        if board[y_start][x_start] != '.':
            return False
        for ofs in self.draws[rotation]:
            x_start += ofs[0]
            y_start += ofs[1]
            if x_start < 0 or y_start < 0 or x_start >= len(board[0]) or y_start >= len(board):
                return False
            if board[y_start][x_start] != '.':
                return False
        return True

    def place(self, board, x_start, y_start, rotation):
        if board[y_start][x_start] != '.':
            raise Exception('Did you check first?')
        board[y_start][x_start] = self.name
        for ofs in self.draws[rotation]:
            x_start += ofs[0]
            y_start += ofs[1]
            if board[y_start][x_start] != '.' and board[y_start][x_start] != self.name:
                raise Exception('Did you check first?')
            board[y_start][x_start] = self.name

    def remove(self, board, x_start, y_start, rotation):
        board[y_start][x_start] = '.'
        for ofs in self.draws[rotation]:
            x_start += ofs[0]
            y_start += ofs[1]
            board[y_start][x_start] = '.'


_ROTS = [
    {'U': [0, -1], 'R':[1, 0], 'D':[0, 1], 'L':[-1, 0], },
    {'U': [1, 0], 'R':[0, 1], 'D':[-1, 0], 'L':[0, -1], },
    {'U': [0, 1], 'R':[-1, 0], 'D':[0, -1], 'L':[1, 0], },
    {'U': [-1, 0], 'R':[0, -1], 'D':[1, 0], 'L':[0, 1], },
    {'U': [0, 1], 'R':[1, 0], 'D':[0, -1], 'L':[-1, 0], },
    {'U': [1, 0], 'R':[0, -1], 'D':[-1, 0], 'L':[0, 1], },
    {'U': [0, -1], 'R':[-1, 0], 'D':[0, 1], 'L':[1, 0], },
    {'U': [-1, 0], 'R':[0, 1], 'D':[1, 0], 'L':[0, -1], },
]

PIECES = [
    Piece('A', 'UUUR',     [244, 117, 33],  [
          0, 3], "-.5,.5 -.5,-2.5 .5,-2.5 1.5,-2.5 1.5,-1.5 .5,-1.5 .5,.5"),
    Piece('B', 'RURU',     [119, 192, 66],  [
          0, 2], "-.5,-.5 .5,-.5 .5,-1.5 1.5,-1.5 1.5,-2.5 2.5,-2.5 2.5,-.5 1.5,-.5 1.5,.5 -.5,.5"),
    Piece('C', 'URRD',     [255, 234, 1],   [0, 1]),
    Piece('D', 'RRDR',     [56, 46, 141],   [0, 0]),
    Piece('E', 'RRUL',     [208, 108, 170], [0, 1]),
    Piece('F', 'LUUL',     [0, 176, 211],   [2, 2]),
    Piece('G', 'RRlDD',    [0, 167, 78],    [0, 0]),
    Piece('H', 'RUdRR',    [113, 55, 31],   [0, 1]),
    Piece('I', 'RRRR',     [60, 123, 191],  [0, 0]),
    Piece('J', 'DDuLrR',   [237, 26, 56],   [1, 0]),
    Piece('K', 'LULrU',    [120, 133, 140], [2, 2]),
    Piece('L', 'RRDD',     [15, 160, 219],  [0, 0]),
]


def get_piece_by_name(name):
    for piece in PIECES:
        if piece.name == name:
            return piece
    return None
