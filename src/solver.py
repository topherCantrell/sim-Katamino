import copy

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
        
def solve(brd, pieces, index, sols, stop_on_first=False):
    """recursive solve"""
    for rot in range(8):        
        for y in range(len(brd)):
            for x in range(len(brd[0])):
                piece = pieces[index]
                if not piece.can_place(brd, x, y, rot):
                    continue
                piece.place(brd, x, y, rot)
                if index == (len(pieces) - 1):
                    b = copy.deepcopy(brd)
                    sols.append(b)                    
                    if stop_on_first:
                        return True
                else:
                    if ok_blanks(brd):
                        resp = solve(brd, pieces, index + 1, sols)
                        if resp and stop_on_first:
                            return True
                piece.remove(brd, x, y, rot)
    return False

def get_unique_solutions(sols):
    pass