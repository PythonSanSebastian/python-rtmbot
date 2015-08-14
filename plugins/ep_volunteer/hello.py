"""
List all available commands
"""
from rtmbot.rtmbot import BOT
from botutils      import hear
from botconfig     import salutes, BotStatus


@hear('[{}]'.format('|'.join(salutes)), channel_type='')
def process_message(data):
    hello = startswithany(salutes, message)
    if hello:
        message = message.replace(hello, '').strip()
        try:
            reply = 'Hello {}.'.format(get_user_name(BOT.slack_client, user_id))
            set_user_status(user_id, BotStatus.hello)
        except Exception as ex:
            reply = 'Ooops, an error occurred {}.'.format(str(ex))
