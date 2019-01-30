
class Piece:

    def __init__(self, name, draw_spec, color):
        self.name = name
        self.draw_spec = draw_spec
        self.color = color
        self.draws = []
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
    Piece('A', 'UUUR', [248, 115, 50]),
    Piece('B', 'RURU', [112, 90, 69]),
    Piece('C', 'URRD', [223, 207, 59]),
    Piece('D', 'RRDR', [61, 35, 112]),
    Piece('E', 'RRUL', [218, 108, 52]),
    Piece('F', 'LUUL', [31, 183, 223]),
    Piece('G', 'RRlDD', [32, 148, 52]),
    Piece('H', 'RUdRR', [121, 68, 50]),
    Piece('I', 'RRRR', [82, 125, 175]),
    Piece('J', 'DDuLrR', [244, 70, 39]),
    Piece('K', 'LULrU', [11, 115, 104]),
    Piece('L', 'RRDD', [19, 148, 191]),
]


def get_piece_by_name(name):
    for piece in PIECES:
        if piece.name == name:
            return piece
    return None
