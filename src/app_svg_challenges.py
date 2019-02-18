from challenges import CHALLENGES
import piece_utils


def print_svg_challenge(challenge, line_num):
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
        if print_info[1] > height:
            height = print_info[1]

    print('<?xml version="1.0" encoding="UTF-8" ?>\n<svg width="{}" height="{}">'.format(
        wid * 10 + 10, height * 10 + 20))
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
        print(g)
        xo = xo + print_info[2] * 10 + 10
    print('</svg>')


print_svg_challenge(CHALLENGES[0], 0)
