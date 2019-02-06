"""
Katamino Simulator
"""

CHALLENGES = [
    {'title':'Small Slam','page':'6','lines': [
        'A3:AHGEBFLD','B3:DECAFHGB','C3:ALEHDCFK','D3:HECDLKBG','E3:ADLFCGHB','F3:ECKHGDAB','G3:ALEFHBDK']
    },
    {'title':'Slam 1','page':'7,8','lines': [
        'A5:','B5:','C5:','D5:','E5:','F5:','G5:',
        'H5:','I5:','J5:','K5:','L5:','M5:','N5:',
        'O6:','P6:','Q6:','R6:','S6:','T6:','U6:',
        'V6:','W6:','X6:','Y6:','Z6',
        'Spades6:','Hearts6:','Diamonds6:','Clubs6:']
    },    
    {'title':'Ultimate Challenges 1', 'page':'9', 'lines': [
        'A4:','B4:','C4:','D4:','E4:','F4:',
        'G4:','H4:','I4:','J4:','K4:','L4:'
    ]},
    {'title':'Ultimate Challenges 2', 'page':'10a', 'lines': [
        'A5:','B5:','C5:','D5:','E5:','F5:',
        'G5:','H5:','I5:','J5:','K5:','L5:'
    ]},
    {'title':'Ultimate Challenges 3', 'page':'10b', 'lines': [
        'A9:','B9:','C9:','D9:','E9:','F9:',
        'G9:','H9:','I9:','J9:','K9:','L9:'
    ]},
    {'title':'Ultimate Challenges 4', 'page':'11', 'lines': [
        'No1_7:','No2_7:','No3_7:','No4_7:','No5_7:',
        'No6_7:','No7_7:','No8_7:','No9_7:','No10_7:',
        'No11_7:','No12_7:','No13_7:','No14_7:','No15_7:',
        'No16_7:','No17_7:','No18_7:','No19_7:','No20_7:',
        'No21_7:','No22_7:','No23_7:','No24_7:','No25_7:',
        'No26_7:','No27_7:','No28_7:','No29_7:','No30_7:',
        'No31_7:','No32_7:','No33_7:','No34_7:','No35_7:',
        'No36_7:','No37_7:','No38_7:','No39_7:','No40_7:',
    ]},
    
]

import copy
import datetime
import pieces
import board


def _rec_blanks(blanks, cur_set, current):
    test_cell = (current[0] + 1, current[1])
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)
    test_cell = (current[0] - 1, current[1])
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)
    test_cell = (current[0], current[1] + 1)
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)
    test_cell = (current[0], current[1] - 1)
    if test_cell in blanks:
        cur_set.append(test_cell)
        del blanks[blanks.index(test_cell)]
        _rec_blanks(blanks, cur_set, test_cell)


def ok_blanks(board):
    blanks = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == '.':
                blanks.append((x, y))
    while blanks:
        cur_set = [blanks[0]]
        del blanks[0]
        _rec_blanks(blanks, cur_set, cur_set[0])
        if len(cur_set) < 5:
            return False

    return True


def solve(brd, pieces, index, out):
    """recursive solver"""
    for rot in range(8):
        if index == 0:
            print('.', end='', flush=True)
        for y in range(len(brd)):
            for x in range(len(brd[0])):
                piece = pieces[index]
                if not piece.can_place(brd, x, y, rot):
                    continue
                piece.place(brd, x, y, rot)
                if index == (len(pieces) - 1):
                    board.write_board(brd, out)
                    out.flush()
                else:
                    if ok_blanks(brd):
                        solve(brd, pieces, index + 1, out)
                piece.remove(brd, x, y, rot)


SMALL_SLAM_3 = [
    '',
    '',
    '',
    '',
    '',
    '',
    ''
]


def main():
    """main"""

    with open('results.txt', 'w') as out:
        num = 0
        for sequence in SMALL_SLAM_3:
            num = num + 1
            pcs = []
            for pos in range(2):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
            pos += 1
            while pos < len(sequence):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
                brd = board.new_board(len(pcs))
                s = str(num) + ': '
                for p in pcs:
                    s = s + p.name
                print(s, end='')
                out.write(s + '\n')
                now = datetime.datetime.now()
                solve(brd, pcs, 0, out)
                after = datetime.datetime.now()

                print((after - now).seconds)
                pos += 1

chal = CHALLENGES[0]
line = chal['lines'][0]
line = line[line.index(':')+1:]
brd = board.new_board(len(line)*6,len(chal['lines'])*6)

for y in range(len(chal['lines'])):
    line = chal['lines'][y]
    line = line[line.index(':')+1:]               
    for x in range(len(line)):
        piece = pieces.get_piece_by_name(line[x])
        piece.place(brd,x*6+piece.print_ofs[0],y*6+piece.print_ofs[1],0)

board.print_board(brd)
