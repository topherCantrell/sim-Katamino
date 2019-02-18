import board_utils
import piece_utils


def get_svg(pn, x, y, r):
    g = piece_utils.get_svg(
        piece_utils.PIECES[pn], 50 + x * 50, 50 + y * 50, r, scale=5, show_origin=False)
    return g


print(get_svg(0, 0, 3, 0))
print(get_svg(1, 0, 4, 0))
print(get_svg(2, 1, 2, 0))
print(get_svg(3, 2, 0, 0))
print(get_svg(4, 2, 4, 0))
print(get_svg(5, 4, 2, 2))
print(get_svg(6, 5, 0, 0))
print(get_svg(7, 6, 3, 0))
print(get_svg(8, 7, 4, 0))
print(get_svg(9, 7, 1, 7))
print(get_svg(10, 11, 3, 0))
print(get_svg(11, 9, 0, 0))
