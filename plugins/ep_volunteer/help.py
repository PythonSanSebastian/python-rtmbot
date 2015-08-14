"""
List all available commands
"""
from rtmbot.rtmbot import BOT
from botutils      import hear
from slack_helpers import get_user_name


@hear('help', channel_type='')
def process_message(data):
    #print(data)
    #print(bot.slack_client.server.users)
    user_id = data.get('user', '')
    return ('How can I help you {}?'.format(get_user_name(user_id, BOT.slack_client)), None)
