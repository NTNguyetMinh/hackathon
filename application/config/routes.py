from __future__ import (
    absolute_import,
    unicode_literals,
)

from application.invite import Invite
from application.notify_result import NotifyResult
from application.start import Start
from application.turn import Turn

def setup_routes(app, db,logger):

    app.add_url_rule('/invite', 'invite', Invite(db, logger).execute, methods=['POST'])
    app.add_url_rule('/start', 'start', Start(db, logger).execute, methods=['POST'])
    app.add_url_rule('/turn', 'turn', Turn(db, logger).execute, methods=['POST'])
    app.add_url_rule('/notify', 'notify_result', NotifyResult(db, logger).execute, methods=['POST'])
