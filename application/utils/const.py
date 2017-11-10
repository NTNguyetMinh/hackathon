
CARRIER = 'CV'
BATTLESHIP = 'BB'
CRUISER = 'CA'
DESTROYER = 'DD'
OIL_RIG = 'OR'

NON_STICK_P = []
STICK_P = [u'cpham30', u'chicken', u'baby']
HISTORY_FIRE = [u'baby', u'chicken', u'paladin']

HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'

DIRECTION = [HORIZONTAL, VERTICAL]
MAX_ATTEMPT = 500

PLAYER_ID = 'tom'
HIT = 'HIT'
MISS = 'MISS'

RANDOM = 1
SCORE = 2

FIND_ALGORITHM = SCORE
STICK_MODE = True
HUNT_MODE = True
HISTORY_MODE = False

CUR_STICK_MODE = False

SHIP = {
    CARRIER: {
        'pieces': 5,
        HORIZONTAL: [
            {'x': 0, 'y': 1},
            {'x': 1, 'y': 1},
            {'x': 2, 'y': 1},
            {'x': 3, 'y': 1},
            {'x': 1, 'y': 0}
        ],
        VERTICAL: [
            {'x': 1, 'y': 0},
            {'x': 1, 'y': 1},
            {'x': 1, 'y': 2},
            {'x': 1, 'y': 3},
            {'x': 0, 'y': 1},
        ]
    },
    BATTLESHIP: {
        'pieces': 4,
        HORIZONTAL: [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0},
            {'x': 3, 'y': 0}
        ],
        VERTICAL: [
            {'x': 0, 'y': 0},
            {'x': 0, 'y': 1},
            {'x': 0, 'y': 2},
            {'x': 0, 'y': 3}
        ]
    },
    CRUISER: {
        'pieces': 3,
        HORIZONTAL: [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0}
        ],
        VERTICAL: [
            {'x': 0, 'y': 0},
            {'x': 0, 'y': 1},
            {'x': 0, 'y': 2}
        ]
    },
    DESTROYER: {
        'pieces': 2,
        HORIZONTAL: [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0}
        ],
        VERTICAL: [
            {'x': 0, 'y': 0},
            {'x': 0, 'y': 1}
        ]
    },
    OIL_RIG: {
        'pieces': 4,
        HORIZONTAL: [
            {'x': 0, 'y': 0},
            {'x': 0, 'y': 1},
            {'x': 1, 'y': 0},
            {'x': 1, 'y': 1}
        ],
        VERTICAL: [
            {'x': 0, 'y': 0},
            {'x': 0, 'y': 1},
            {'x': 1, 'y': 0},
            {'x': 1, 'y': 1}
        ]
    }
}
