PIECES = [{
    'name': 'A',
    'shape': """
AA
A.
A.
A.
""",
    'color': [244, 117, 33],
}, {
    'name': 'B',
    'shape': """
..B
.BB
BB.
""",
    'color': [119, 192, 66],
}, {
    'name': 'C',
    'shape': """
CC
.C
CC
""",
    'color': [255, 234, 1],
}, {
    'name': 'D',
    'shape': """
.D
.D
DD
D.
""",
    'color': [56, 46, 141],
}, {
    'name': 'E',
    'shape': """
E.
EE
EE
""",
    'color': [208, 108, 170],
}, {
    'name': 'F',
    'shape': """
FF.
.F.
.FF
""",
    'color': [0, 176, 211],
}, {
    'name': 'G',
    'shape': """
GGG
.G.
.G.
""",
    'color': [0, 167, 78],
}, {
    'name': 'H',
    'shape': """
H.
HH
H.
H.
""",
    'color': [113, 55, 31],
}, {
    'name': 'I',
    'shape': """
I
I
I
I
I
""",
    'color': [60, 123, 191],
}, {
    'name': 'J',
    'shape': """
.J.
JJJ
.J.
""",
    'color': [237, 26, 56],
}, {
    'name': 'K',
    'shape': """
.K.
KK.
.KK
""",
    'color': [120, 133, 140],
}, {
    'name': 'L',
    'shape': """
LLL
..L
..L
""",
    'color': [15, 160, 219],
}]

def flip(piece):
    """
    Create a new piece that is flipped along the X axis from the given piece.
    Arguments:
        piece : 2D array -- the ascii representation of the given piece
    Returns:
        2D array -- the ascii representation of the new piece
    """
    # Yes, there is some slice magic I could use here instead
    ret = []
    for y in range(len(piece)-1,-1,-1):
        ret.append(piece[y])
    return ret

def turn(piece,dist):
    """
    Create a new piece that is a clockwise rotation of the given piece.
    The number of turns is passed in, thus "3" is actually 1 rotation
    counterclockwise.
    Arguments:
        piece : 2D array -- the ascii representation of the given piece
    Returns:
        2D array -- the ascii representation of the new piece
    """
    if dist==0:
        # This makes us return a new piece same as the old
        dist = 4
    for _ in range(dist):
        ret = []
        for x in range(len(piece[0])):
            nr = []
            for y in range(len(piece)-1,-1,-1):
                nr.append(piece[y][x])
            ret.append(nr)
        piece = ret
    return ret

def init():
    """Initialize all pieces

    Add 'rotates' (set of uniques pieces) and 'rotates_names' (flip/rotate of each
    unique piece).
    """
    for p in PIECES:
        name = p['name']
        # Convert the string-shape to a 2D array (official "piece" structure)
        shape = p['shape'].split()        
        org = []        
        for row in shape:
            nr = []
            for col in row:
                nr.append(col)
            org.append(nr)
        # Run flips and rotations to find the unique orientations
        ps = []
        pr = []
        for i in range(4):
            np = turn(org,i)
            if np not in ps:
                ps.append(np)
                pr.append(name+str(i))
        name = name.lower()
        org = flip(org)
        for i in range(4):
            np = turn(org,i)
            if np not in ps:
                ps.append(np)
                pr.append(name+str(i))
        p['rotates'] = ps
        p['rotates_names'] = pr
        #print(p['rotates_names'])

def get_piece(name):
    for p in PIECES:
        if p['name'] == name:
            return p