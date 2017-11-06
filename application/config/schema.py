from __future__ import (
    absolute_import,
    unicode_literals,
)

schema_invite = {
    "type": "object",
    "properties": {
        'sessionId': {'type': 'string'},
        'gameRule': {
            'type': 'object',
            'properties': {
                'boardWidth' : {'type': 'integer'},
                'boardHeight': {'type': 'integer'},
                'ships': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'type': {'type': 'string'},
                            'quantity': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
}

schema_start = {
    'type': 'object',
    'properties': {
        'sessionId': {'type': 'string'},
        'player1': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'}
            }
        },
        'player2': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'}
            }
        }
    }
}

schema_turn = {
    'type': 'object',
    'properties': {
        'sessionId': {'type': 'string'},
        'turnNumber': {'type': 'integer'}
    }
}

schema_notify = {
    'type': 'object',
    'properties': {
        'sessionId': {'type': 'string'},
        'shotResult': {
            'type': 'object',
            'properties': {
                'playerId': {'type': 'string'},
                'position': {
                    'type': 'object',
                    'properties': {
                        'x': {'type': 'integer'},
                        'y': {'type': 'integer'}
                    }
                },
                'status': {'type': 'string'},
                'recognizedWholeShip': {
                    'type': 'object',
                    'properties': {
                        'type': {'type': 'string'},
                        'positions': {
                            'type': 'array',
                            'items': {
                                'x': {'type': 'integer'},
                                'y': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
}