
class UserStatus(object):

    def __init__(self):
        self._user_status = {}

    def set(self, user_id, status):
        if not user_id:
            return
        self._user_status[user_id] = status

    def get(self, user_id):
        return self._user_status[user_id]

    def reset(self, user_id):
        del self._user_status[user_id]

def startswithany(prefixes, text):
    for prefix in prefixes:
        if text.startswith(prefix):
            return prefix
    return ''
