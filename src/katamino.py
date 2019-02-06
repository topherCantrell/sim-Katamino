"""
Katamino Simulator
"""

import copy
import datetime

import board
import pieces

# These are the challenges as listed in the manual
CHALLENGES = [
    {'title': 'Small Slam', 'page': '6', 'lines': [
        'A3:AHGEBFLD', 'B3:DECAFHGB', 'C3:ALEHDCFK', 'D3:HECDLKBG', 'E3:ADLFCGHB', 'F3:ECKHGDAB', 'G3:ALEFHBDK']
     },
    {'title': 'Slam 1', 'page': '7,8', 'lines': [
        'A5:AECKBHFDL', 'B5:HDECFLGAK', 'C5:AHLGBFKCE', 'D5:DLECKBAFG', 'E5:AHDEBGLKC', 'F5:AECFGKDBH', 'G5:ALECBDHGF',
        'H5:ADEGBFHKL', 'I5:AHLCFKBDG', 'J5:ALEKBHCGD', 'K5:AHDCBKELF', 'L5:HLEFBDKGC', 'M5:AHLEKCGFB', 'N5:AHEFBDCLG',
        'O6:AHDCKGFE',  'P6:ADLEFKGH',  'Q6:AHEFKBLC',  'R6:ADLECGBK',  'S6:HLECGBAF',  'T6:AHLFKGEB',  'U6:ADLECKFG',
        'V6:DLECFGKH',  'W6:DLECFKHB',  'X6:HDLEGBFC',  'Y6:ADCFKGLH',  'Z6:AHEKGBCF',
        'Spades6:HDECFGKB', 'Hearts6:ADLCKBHG', 'Diamonds6:ADLEKGBF', 'Clubs6:ALECKGDH']
     },
    {'title': 'Ultimate Challenges 1', 'page': '9', 'lines': [
        'A4:ADLFCGEJKIB', 'B4:AHCKFLJEIDG', 'C4:AHLEKBDCFGI', 'D4:HECKGJALBFD', 'E4:AHEFBDGKICJ', 'F4:AECKJHIDGBL',
        'G4:AHEBDCLFJIK', 'H4:HDLGKIFBAJC', 'I4:ALEFDKBIDGJ', 'J4:AHEGBDILCJF', 'K4:HDECLFJIBKG', 'L4:AHLCFIKGJEB'
    ]},
    {'title': 'Ultimate Challenges 2', 'page': '10a', 'lines': [
        'A5:ADEGBFLICHK', 'B5:AHDLEGBJKIF', 'C5:AECKBIFDLGJ', 'D5:HDECFAJLGBI', 'E5:HLEFBDGIJCK', 'F5:DLECKJHAIGB',
        'G5:AECGJKDFHLI', 'H5:ALEKBICGJFH', 'I5:AECFGHIJDKB', 'J5:AHLGBFKICJD', 'K5:ADECFJIHBKL', 'L5:ALECBHJKFDG'
    ]},
    {'title': 'Ultimate Challenges 3', 'page': '10b', 'lines': [
        'A9:IAHDLECFK', 'B9:HLECFKGBJ', 'C9:IADLEFKGJ', 'D9:IAHECKGBJ', 'E9:IDLECFKGB', 'F9:IAHDLECBJ',
        'G9:IHDECFKGJ', 'H9:IAHDLKGBJ', 'I9:AHDLCFKGJ', 'J9:IAHDLEFGB', 'K9:IALECFGBJ', 'L9:IAHDCFKBJ'
    ]},
    {'title': 'Ultimate Challenges 4', 'page': '11', 'lines': [
        'No1_7:IAHECBJGLK',  'No2_7:AHEFKGBJDC',  'No3_7:IADLCFGHKE',  'No4_7:AHEKGBJIFL',  'No5_7:IHDLCKBAEJ',
        'No6_7:ALEKGBJFCD',  'No7_7:HDECFKGLJI',  'No8_7:IADECGJBFH',  'No9_7:ILECFKBDHA',  'No10_7:IHDLCGJKBF',
        'No11_7:IADEFGBKJC', 'No12_7:IHDLCFKGBA', 'No13_7:AHLCFKBJID', 'No14_7:DLECKGJHAB', 'No15_7:IAHLCKBEFJ',
        'No16_7:AHLEFBJGCI', 'No17_7:IHECFGBDLK', 'No18_7:IDLECKJBGF', 'No19_7:ADEFKGBLJH', 'No20_7:IADEFKGJHL',
        'No21_7:IDLECFGJAB', 'No22_7:IAHCKGBFDJ', 'No23_7:HDLEFKGBJC', 'No24_7:IAHDCGJLFE', 'No25_7:IHDLEKBJGF',
        'No26_7:AHLCKGJDBI', 'No27_7:IAHECFBJKG', 'No28_7:ADLEKGBCIH', 'No29_7:IALECFJKBD', 'No30_7:IHLCFGBEJK',
        'No31_7:AHDEKGBJIF', 'No32_7:IHECFKGDBJ', 'No33_7:AHDLEFBJKI', 'No34_7:IAHCKGJFDL', 'No35_7:IHDLCGBEJK',
        'No36_7:ADLCGBJIKE', 'No37_7:IAECKGBFLH', 'No38_7:IADCFKGLJB', 'No39_7:AHDLCKJBFG', 'No40_7:IALEFGBJHD',
    ]},

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


chal = CHALLENGES[5]
line = chal['lines'][0]
line = line[line.index(':') + 1:]
brd = board.new_board(len(line) * 6, len(chal['lines']) * 6)

for y in range(len(chal['lines'])):
    line = chal['lines'][y]
    line = line[line.index(':') + 1:]
    for x in range(len(line)):
        piece = pieces.get_piece_by_name(line[x])
        piece.place(
            brd, x * 6 + piece.print_ofs[0], y * 6 + piece.print_ofs[1], 0)

board.print_board(brd)
