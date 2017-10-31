from __future__ import (
    absolute_import,
    unicode_literals,
)

from application.invite import Invite
from application.notify_result import NotifyResult
from application.start import Start
from application.turn import Turn

def setup_routes(app):

    app.add_url_rule('/invite', 'invite', Invite().execute, methods=['POST'])
    app.add_url_rule('/start', 'start', Start().execute, methods=['POST'])
    app.add_url_rule('/turn', 'turn', Turn().execute, methods=['POST'])
    app.add_url_rule('/notify_result', 'notify_result', NotifyResult().execute, methods=['POST'])