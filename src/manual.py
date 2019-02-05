import struct

# http://www.ninivegames.com/Manuals/English/545-Katamino.pdf

pixels = []
row = []
pixels.append(row)
row_num = 0

fname = 'man6_8x7_3.TXT'

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

        row.append((x, y, r, g, b))

WIDTH = 8
HEIGHT = 7

cell_width = int(len(pixels[0]) / WIDTH)
ofs_width = int(cell_width / 2)
cell_height = int(len(pixels) / HEIGHT)
ofs_height = int(cell_height / 2)

for y in range(HEIGHT):
    for x in range(WIDTH):
        print(pixels[ofs_height + y * cell_height][ofs_width + x * cell_width])
