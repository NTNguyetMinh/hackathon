from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from flask import request

class Start(object):

    def execute(self):
        body = request.get_json()

        return json.dumps({'result': True})

