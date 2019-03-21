import piece_utils

for p in piece_utils.PIECES:
    print('piece_draws.clear();')
    for u in p['unique']:
        s = p['draws'][u]
        print('piece_draws.push_back("' + s + '");')
