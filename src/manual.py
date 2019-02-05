import struct
import pieces

# http://www.ninivegames.com/Manuals/English/545-Katamino.pdf

known_colors = []
for piece in pieces.PIECES:
    known_colors.append(piece.color)

pixels = []
row = []
pixels.append(row)
row_num = 0


WIDTH = 10
HEIGHT = 10
OFS = 8
fname = 'man11d_10x10_7.TXT'

with open('../art/manual/' + fname) as f:
    for g in f:
        g = g.strip()
        if g[0] == '#':
            continue
        i = g.index('#')
        g = g[0:i].strip()
        g = g.replace(':', ',')
        g = g.replace('(', '')
        g = g.replace(')', '')
        frags = g.split(',')

        x = int(frags[0].strip())
        y = int(frags[1].strip())
        r = int(frags[2].strip())
        g = int(frags[3].strip())
        b = int(frags[4].strip())

        if y != row_num:
            row = []
            pixels.append(row)
            row_num = y

        if [r, g, b] not in known_colors:
            r = 255
            g = 255
            b = 255

        row.append((x, y, r, g, b))


cell_width = int(len(pixels[0]) / WIDTH)
ofs_width = int(cell_width / 2)
cell_height = int(len(pixels) / HEIGHT)
ofs_height = int(cell_height / 2)


for y in range(HEIGHT):
    for x in range(WIDTH):
        colors = []
        xo = ofs_width + x * cell_width
        yo = ofs_height + y * cell_height
        for i in range(xo - OFS, xo + OFS):
            for j in range(yo - OFS, yo + OFS):
                pix = pixels[j][i]
                col = pix[2:]
                if not col in colors and col != (255, 255, 255):
                    colors.append(col)
        print(colors)
