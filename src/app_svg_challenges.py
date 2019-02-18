from challenges import CHALLENGES
import piece_utils


def get_svg_challenge(challenge, line_num):
    ret = ''
    description = challenge['lines'][line_num]
    piece_names = description[description.index(':') + 1:]
    wid = 0
    height = 0
    for p in piece_names:
        piece = piece_utils.get_piece_by_id(ord(p) - 64)
        print_pref = piece['print_pref']
        print_info = piece['print_info'][print_pref]
        piece = piece_utils.get_piece_by_id(ord(p) - 64)
        wid = wid + print_info[2] + 1
        if print_info[3] > height:
            height = print_info[3]

    ret = ret + ('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">'.format(
        wid * 10 + 10, height * 10 + 10))
    xo = 10
    yo = 10
    for p in piece_names:
        piece = piece_utils.get_piece_by_id(ord(p) - 64)
        print_pref = piece['print_pref']
        print_info = piece['print_info'][print_pref]
        g = piece_utils.get_svg(
            piece, xo + print_info[0] * 10, yo +
            print_info[1] * 10, print_pref,
            show_origin=False)
        ret = ret + (g)
        xo = xo + print_info[2] * 10 + 10
    ret = ret + ('</svg>')
    return ret


for challenge in CHALLENGES:
    title = challenge['title'].replace(' ', '_')
    for n in range(len(challenge['lines'])):
        line = challenge['lines'][n]
        i = line.index(':')
        cn = line[:i].replace('-', '_')
        fname = title + '_' + cn
        with open('../art/' + fname + '.svg', 'w') as f:
            f.write(get_svg_challenge(challenge, n))
