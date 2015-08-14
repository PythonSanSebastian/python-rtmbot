"""
Helper functions to use the Slack Client
"""

def get_user_name(user_id, slack_client):
    """Returns the username"""
    user = slack_client.server.users.find(user_id)
    return user.name


def get_user_email(user_id, slack_client):
    user = slack_client.server.users.find(user_id)
    return user.email


def get_channel_name(channel_id, slack_client):
    channel = slack_client.server.channels.find(channel_id)
    return channel.name
