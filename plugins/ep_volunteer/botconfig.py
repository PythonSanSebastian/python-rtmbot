
from enum import Enum

botname = 'bob'
hellos  = ['Hi {}', 'Hey {}', 'Hello {}', '{}']
salutes = [hello.format(botname) for hello in hellos]


class BotStatus(Enum):
    hello = 1
