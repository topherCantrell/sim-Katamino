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
import datetime

board = [0]*256

pieces = [
    
    #     A
    # XX
    # X
    # X
    # @
    [
        [-16,-16,-16,1],  [1,1,1,16],  [16,16,16,-1], [-1,-1,-1,-16],
        [-16,-16,-16,-1], [1,1,1,-16], [16,16,16,1],  [-1,-1,-1,16],
    ],
    
    #     B
    #   X
    #  XX
    # @X
    [
        [1,-16,1,-16],[16,1,16,1],[-1,16,-1,16],[-16,-1,-16,-1]
    ],
    
    #     C
    # XXX
    # X X
    [
        [1,16,16,-1],[-1,16,16,1],[-16,1,1,16],[16,1,1,-16]
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
        [1,16,16,1], [16,-1,-1,16], [-1,-16,-16,-1], [-16,1,1,-16],
        [1,-16,-16,1], [16,1,1,16], [1,-16,-16,1], [16,1,1,16]
    ],
    
    #     G
    # XXX
    #  X
    #  X
    [    
        [-16,-16-1,1,1], [1,1+16,-16,-16], [16,16-1,1,1],[-1,-1-16,16,16]
    ],
    
    #     H
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
        [-16,-1,1-16,1],[1,-16,1+16,16],[16,1,-1+16,-1],[-1,16,-16-1,-16]
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
    global board
    board = [0]*256    
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

DOTSON = 0
DOTSCOL = 0
def sim(data):
    global DOTSON,DOTSCOL    
    DOTSCOL = 0
    total_num = data[0]
    cur_ind = total_num*4+1 # cur    
    while True:
        # This is the moving piece
        try:
            pn = data[cur_ind]
            drw = [data[pn*4+1],data[pn*4+2],data[pn*4+3],data[pn*4+4]]
        except:
            print(pn)
            print(data)
            raise
        
            
        # Piece's current position (erase it if visible)
        cp = data[cur_ind+pn+1]        
        # Get the next position (if any)
        
        if data[cur_ind] <= DOTSON:
            print(f'{data[cur_ind]}|',end='')     
            DOTSCOL+=1
            if DOTSCOL==80:
                DOTSCOL = 0
                print()       
                
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

def show_board(map):
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
                c = map[c-65]#chr(c)
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
            
def make_combos(num):
    ret = []
    for i in range(4096):
        s = '{:012b}'.format(i)
        if len(s.replace('0', '')) == num:
            t = []
            for j in range(12):
                if s[j] == '1':
                    t.append(chr(65+j))
            t = ''.join(sorted(t))
            if not t in ret:
                ret.append(t)
    ret.sort()
    return ret

def get_slides(spec):
    num = len(spec)
    pis = []
    ptr = [0]*num    
    for s in spec:
        pis.append(pieces[ord(s)-65])
        
    #ret = []        
    
    while True:         
        
        # Append this combination
        cur = []
        for i in range(num):
            cur.append(pis[i][ptr[i]])
        #ret.append(cur)
        yield (cur,ptr)
                      
        has_next = False          
        for i in range(len(ptr)-1,-1,-1):
            ptr[i] +=1
            if ptr[i]<len(pis[i]):
                has_next = True
                break
            ptr[i] = 0
            
        if not has_next:
            #return ret        
            return
        
def show_all_pieces():
    
    global board
    
    # A   
    board = [0]*256
    place_piece(6*16+9,65,pieces[0][0])
    place_piece(8*16+9,65,pieces[0][1])
    place_piece(8*16+6,65,pieces[0][2])
    place_piece(6*16+6,65,pieces[0][3])
    show_board('ABC')  
    print()
    board = [0]*256
    place_piece(6*16+9,65,pieces[0][4])
    place_piece(8*16+9,65,pieces[0][5])
    place_piece(8*16+6,65,pieces[0][6])
    place_piece(6*16+6,65,pieces[0][7])
    show_board('ABC')  
    print()
            
    # B
    board = [0]*256
    place_piece(6*16+9,66,pieces[1][0])
    place_piece(8*16+9,66,pieces[1][1])
    place_piece(8*16+6,66,pieces[1][2])
    place_piece(6*16+6,66,pieces[1][3])
    show_board('ABC')
    print()
    
    #C
    board = [0]*256
    place_piece(1*16+1,67,pieces[2][0])
    place_piece(1*16+5,67,pieces[2][1])
    place_piece(6*16+1,67,pieces[2][2])
    place_piece(8*16+1,67,pieces[2][3])
    show_board('ABC')
    print()
    
    # D   
    board = [0]*256
    place_piece(6*16+9,68,pieces[3][0])
    place_piece(8*16+9,68,pieces[3][1])
    place_piece(8*16+6,68,pieces[3][2])
    place_piece(6*16+6,68,pieces[3][3])
    show_board('ABCD')  
    print()
    board = [0]*256
    place_piece(6*16+9,68,pieces[3][4])
    place_piece(8*16+9,68,pieces[3][5])
    place_piece(8*16+6,68,pieces[3][6])
    place_piece(6*16+6,68,pieces[3][7])
    show_board('ABCD')  
    print()
    
    # E   
    board = [0]*256
    place_piece(1*16+1,69,pieces[4][0])
    place_piece(3*16+10,69,pieces[4][1])
    place_piece(10*16+1,69,pieces[4][2])
    place_piece(10*16+10,69,pieces[4][3])
    show_board('ABCDE')  
    print()
    board = [0]*256
    place_piece(1*16+2,69,pieces[4][4])
    place_piece(3*16+10,69,pieces[4][5])
    place_piece(10*16+2,69,pieces[4][6])
    place_piece(10*16+10,69,pieces[4][7])
    show_board('ABCDE')  
    print()
    
    # F   
    board = [0]*256
    place_piece(1*16+1,70,pieces[5][0])
    place_piece(8*16+3,70,pieces[5][1])
    place_piece(8*16+9,70,pieces[5][2])
    place_piece(4*16+8,70,pieces[5][3])
    show_board('ABCDEF')  
    print()
    board = [0]*256
    place_piece(5*16+2,70,pieces[5][4])
    place_piece(8*16+3,70,pieces[5][5])
    place_piece(10*16+9,70,pieces[5][6])
    place_piece(4*16+8,70,pieces[5][7])
    show_board('ABCDEF')  
    print()
    
    # G   
    board = [0]*256
    place_piece(3*16+2,71,pieces[6][0])
    place_piece(3*16+8,71,pieces[6][1])
    place_piece(8*16+7,71,pieces[6][2])
    place_piece(8*16+4,71,pieces[6][3])
    show_board('ABCDEFG')  
    print()
    
    # H   
    board = [0]*256
    place_piece(2*16+2,72,pieces[7][0])
    place_piece(2*16+12,72,pieces[7][1])
    place_piece(8*16+6,72,pieces[7][2])
    place_piece(12*16+3,72,pieces[7][3])
    show_board('ABCDEFGH')  
    print()
    board = [0]*256
    place_piece(2*16+2,72,pieces[7][4])
    place_piece(2*16+12,72,pieces[7][5])
    place_piece(12*16+3,72,pieces[7][6])
    place_piece(6*16+6,72,pieces[7][7])
    show_board('ABCDEFGH')  
    print()
    
    # I   
    board = [0]*256
    place_piece(1*16+1,73,pieces[8][0])
    place_piece(8*16+9,73,pieces[8][1])
    show_board('ABCDEFGHI')  
    print()
    
    # J
    board = [0]*256
    place_piece(7*16+7,74,pieces[9][0])
    show_board('ABCDEFGHIJ')  
    print()       
    
    # K   
    board = [0]*256
    place_piece(6*16+9,75,pieces[10][0])
    place_piece(8*16+9,75,pieces[10][1])
    place_piece(8*16+6,75,pieces[10][2])
    place_piece(6*16+6,75,pieces[10][3])
    show_board('ABCDEFGHIJK')  
    print()
    board = [0]*256
    place_piece(5*16+10,75,pieces[10][4])
    place_piece(8*16+9,75,pieces[10][5])
    place_piece(8*16+6,75,pieces[10][6])
    place_piece(5*16+5,75,pieces[10][7])
    show_board('ABCDEFGHIJK')  
    print()
    
    # L
    board = [0]*256
    place_piece(2*16+2,76,pieces[11][0])
    place_piece(2*16+13,76,pieces[11][1])
    place_piece(9*16+2,76,pieces[11][2])
    place_piece(8*16+13,76,pieces[11][3])
    show_board('ABCDEFGHIJKL')  
    print()
 
#show_all_pieces()       
  
start = datetime.datetime.now()
print(start)
#brd = 'ABCDEFGHIJKL'

# TODO: there are two solutions for this. But this code only finds one.
#brd = 'ABEGH'
brd = 'ABCDEFGHIJKL'
slides = get_slides(brd)
#print(f'Total slides: {len(slides)}')

# A(0:8) B(0:4) C(0:6)

for s,ptr in slides:
    print(ptr)
    
    test = [len(s)]
    for p in s:
        test = test + p
    test.append(0)
    test = test + [255]*len(s)
        
    clear_board(len(brd))
    res = sim(test)     
    print()
    if res:        
        show_board(brd)
        
        
print('FROM',start)
print('TO',datetime.datetime.now())



#test = [3] + pieces[0][0] + pieces[6][2] + pieces[7][6] + [0,255,255,255]

#print(len(s))
#print(len(s[0]))

#d = make_combos(11)
#print(d)
# This configuration is the first easy solution        
#test = [4] + pieces[0][0] + pieces[1][3] + pieces[2][1] + pieces[3][7] + [0,255,255,255,255]

#clear_board(3)
#test = [3] + pieces[0][0] + pieces[6][2] + pieces[7][6] + [0,255,255,255]
#sim(test)
#show_board()

#while True:
#    res = sim(test)
#    if res:
#        show_board()
#    else:
#        break




