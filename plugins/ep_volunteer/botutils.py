"""
Helper functions to improve the interface to create plugins.
"""

import logging
import re

from   botconfig     import botname, BotStatus
from   users         import UserStatus

outputs  = []
crontabs = []
user_status = UserStatus()

log = logging.getLogger(__name__)


def hear(msg_regx, channel_type='D'):
    def wrap(f):
        def wrapped_f(*args):
            log.debug('Received: {}.'.format(args))

            data    = args[0]
            channel = data.get("channel", '')
            message = data.get("text",    '')
            user_id = data.get("user",    '')

            if not message or not channel.startswith(channel_type):
                return

            reply = ''
            crons = ''
            if re.match(msg_regx, message):
                try:
                    reply, crons = f(data)
                except Exception as ex:
                    log.exception('Error processing message.')
                    reply = 'Ooops, an error occurred {}.'.format(str(ex))
                    user_status.reset(user_id)

            if reply or crons:
                outputs.append([channel, reply])
                crontabs.append(crons)
        return wrapped_f
    return wrap
