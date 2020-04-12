"""

Board is 16x16 bytes. FFs top border. FEs right boarder.
the boarder.

#####...........
#...|...........
#...|...........
#...|...........
#...|...........
#...|...........
#####...........
................

Pieces are lists of offsets to draw.

Data for a single simulation:
  num, a1,b1,c1,d1, a2,b2,c2,d2, a3,b3,c3,d3, cur, p1, p2, p3
  
  num         = number of pieces
  a1,b1,c1,d1 = draw list for each piece
  cur         = cursor to piece in progress
  p1          = board positions for all pieces (-1 for not-placed)

"""

board = [0]*256

pieces = [
    
    #     A
    # XX
    # X
    # X
    # X
    [
        [-16,-16,-16,1],  [1,1,1,16],  [16,16,16,-1], [-1,-1,-1,-16],
        [-16,-16,-16,-1], [1,1,1,-16], [16,16,16,1],  [-1,-1,-1,16],
    ],
    
    #     B
    #   X
    #  XX
    # XX
    [
        [1,-16,1,-16],[16,1,16,1],[-16,1,-16,1],[-16,-1,-16,-1]
    ],
    
    #     C
    # XXX
    # X X
    [
        [1,16,16,-1],[-1,16,16,1],[16,1,1,-16],[-16,1,1,16]
    ],
    
    #     D
    # XXX
    #   XX
    [
        [1,1,16,1], [16,16,-1,16], [-1,-1,-16,-1], [-16,-16,1,-16],
        [1,1,-16,1], [16,16,1,16], [-1,-1,16,-1], [-16,-16,-1,-16]
    ],
    
    #     E
    #  XX
    # XXX
    [
        [16,16,1,-16],[1,1,-16,-1],[-16,-16,-1,16],[-1,-1,16,1],
        [16,16,-1,-16],[1,1,16,-1],[-16,-16,1,16],[-1,-1,-16,1]
    ],
    
    #     F
    # XX
    #  X
    #  XX
    [
        [1,16,16,1], [16,-1,-1,16], [-1,-16,-16,-1], [-16,1,1,-16]
    ],
    
    #     G
    # XXX
    #  X
    #  X
    [    
        [-16,-16-1,1,1], [1,1+16,-16,-16], [16,16-1,1,1],[-1,-1-16,16,16]
    ],
    
    #  X
    # XXXX
    [
        [16,16,-1,1+16], [-1,-1,-16,16-1], [-16,-16,1,-1-16], [1,1,16,-16+1],
        [16,16,1,-1+16], [-1,-1,16,-16-1], [-16,-16,-1,1-16], [1,1,-16,16+1]
    ],
    
    #     I
    # XXXXX
    [
        [1,1,1,1], [16,16,16,16]
    ],
    
    #     J
    #  X
    # XXX
    #  X
    [
        [-1,1+16,1-16,-1-16]
    ],
    
    #     K
    #  X
    # XX
    #  XX
    [
        [-16,1,-1-16,-1],[1,16,1-16,-16],[16,-1,16+1,1],[-1,-16,16-1,16],
        [-16,-1,1-16,1],[1,-16,1+16,16],[16,1,-1,16,-1],[-1,16,-16-1,-16]
    ],    
    
    #     L
    # XXX
    #   X
    #   X
    [
        [1,1,16,16],[-1,-1,16,16],[1,1,-16,-16],[-1,-1,-16,-16]
    ]
    
]
        
def clear_board(cols):
    for i in range(cols+2):
        board[i] = 255
        board[i+16*6] = 255
    for i in range(5):
        board[16*i+16]= 255
        board[16*i+16+cols+1]= 254

def place_piece(pos,n,drw):
    if n is None:
        if board[pos]!=0:
            return False       
    else:
        board[pos] = n
    for offs in drw:
        pos = pos + offs
        if n is None:
            if board[pos]!=0:
                return False
        else:
            board[pos] = n    
    return True

def next_available(pos,drw):
    if pos==255:
        # Start from the beginning
        pos = 16
    while True:
        pos = pos + 1
        if board[pos]==255:
            # No spot found
            return 255
        if board[pos]==254:
            # Back to the start of the next row
            pos = (pos & 0xF0) + 16
            continue
        if place_piece(pos,None,drw):
            return pos   

def sim(data):
    total_num = data[0]
    cur_ind = total_num*4+1 # cur    
    while True:
        # This is the moving piece
        pn = data[cur_ind]
        drw = [data[pn*4+1],data[pn*4+2],data[pn*4+3],data[pn*4+4]]
        # Piece's current position (erase it if visible)
        cp = data[cur_ind+pn+1]        
        # Get the next position (if any)        
        np = next_available(cp,drw)     
        data[cur_ind+pn+1]=np   
        if np==255:            
            pn -= 1
            if pn<0:
                # Nothing to back up to. We are done.
                return False
            if cp!=255:
                place_piece(cp,0,drw)                
            data[cur_ind] = pn
            continue
        
        # There was a spot ... draw it
        if cp!=255:
            place_piece(cp,0,drw)
        place_piece(np,65+pn,drw)
                
        pn += 1
        if pn==total_num:
            return True
        data[cur_ind] = pn            

def show_board():
    for y in range(16):
        for x in range(16):
            c = board[y*16+x]
            if c==0:
                c = '.'
            elif c==255:
                c = '#'
            elif c==254:
                c = '|'
            else:
                c = chr(c)
            print(c,end='')
        print()
                
def show_pieces():
    for pn in range(12):
        print(chr(pn+65))
        for i in range(len(pieces[pn])):
            board = [0]*256
            place_piece(7*16+7,65+pn,pieces[pn][i])
            show_board()
            print()

# This configuration is the first easy solution        
#test = [4] + pieces[0][0] + pieces[1][3] + pieces[2][1] + pieces[3][7] + [0,255,255,255,255]

#clear_board(4)

#while True:
#    res = sim(test)
#    if res:
#        show_board()
#    else:
#        break




