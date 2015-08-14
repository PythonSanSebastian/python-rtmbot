#!/usr/bin/env python

import glob
import yaml
import json
import os
import os.path as op
import sys
import time
import logging
from   slackclient import SlackClient

from   .job    import Job
from   .plugin import Plugin


# init logger
log = logging.getLogger(__name__)


# module global variables
#SITE_PLUGINS      = []
#FILES_DOWNLOADING = []
#JOB_HASH          = {}
BOT               = []

class RtmBot(object):

    def __init__(self, token, ping_freq=3):
        self.last_ping    = 0
        self.token        = token
        self.bot_plugins  = []
        self.slack_client = None
        self._ping_freq   = ping_freq

    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()

    def start(self):
        self.connect()
        #self.load_plugins()
        while True:
            for reply in self.slack_client.rtm_read():
                self.input(reply)
            self.crons()
            self.output()
            self.autoping()
            time.sleep(.1)

    def autoping(self):
        #hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + self._ping_freq:
            self.slack_client.server.ping()
            self.last_ping = now

    def input(self, data):
        if "type" in data:
            # TODO: this logic in function calling is okay, but it does not allow me
            # to call different functions in the same file (no overloading allowed).
            # An approach with decorators would be much better.
            function_name = "process_" + data["type"]
            log.debug("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)

    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel != None and output[1] != None:
                    if limiter == True:
                        time.sleep(.1)
                        limiter = False
                    message = output[1].encode('ascii', 'ignore')
                    channel.send_message("{}".format(message))
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()

    def load_plugins(self, plugins_folder):
        for plugin in glob.glob(op.join(plugins_folder, '*')):
            if op.isdir(plugin):
                sys.path.insert(0, plugin)

        sys.path.insert(0, plugins_folder)

        plugin_files  = glob.glob(op.join(plugins_folder, '*.py'))
        plugin_files += glob.glob(op.join(plugins_folder, '*', '*.py'))

        for plugin in plugin_files:
            log.info('Loading {}'.format(plugin))
            name = op.basename(plugin).replace('.py', '')
            try:
                self.bot_plugins.append(Plugin(name, {'bot': self}))
            except:
                log.exception("Error loading plugin {}.".format(plugin))
                raise


def setup_bot(token, workdir, ping_freq):
    """ Set up the global BOT.

    Parameters
    ----------
    token: str
        Slack auth token

    workdir: str
        Path to where the plugins folder is.

    ping_freq: int
        Frequency of pings to Slack of the bot.
    """
    global BOT

    log.debug(workdir)
    try:
        BOT = RtmBot(token, ping_freq=ping_freq)
        BOT.load_plugins(workdir)
        log.debug('Bot initialized.')
    except Exception as exc:
        log.exception('Error setting the bot.')
        raise
