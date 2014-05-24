raw_positions = {
        'logo': (2621, 404),
        'menu play': (2627, 522),
        'tournament': (2627, 590),
        'pool shop': (2627, 645),
        'spin & win': (2292, 365),
        'scratch & win': (2292, 427),
        'collect 25 coins': (2917, 360),
        'left arrow': (2306, 549),
        'right arrow': (2947, 549),
        '1v1 play': (2629, 755),
        '1v1 back to main screen': (2393, 756),
        'game top left': (2252, 291),
        'game bottom right': (3001, 811),
        'table top left': (2338, 423),
        'table bottom right': (2913, 710),
        'player status top left': (2506, 294),
        'player status bottom right': (2585, 373),
        }

def get_position(known_position_name, known_position, query_position_name):
    a = raw_positions[known_position_name]
    b = raw_positions[query_position_name]
    c = known_position
    return (c[0]-a[0]+b[0], c[1]-a[1]+b[1])
