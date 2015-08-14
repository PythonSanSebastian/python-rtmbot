#!/usr/bin/env python

import sys
import yaml
import os.path as op
import argparse
import logging

from   .rtmbot import setup_bot
from   .logger import setup_logging

log = logging.getLogger(__name__)


def start_bot(token, workdir, daemon=False, ping_freq=3):
    """ Starts the main loop of the RtmBot

    Parameters
    ----------
    token: str
        Slack auth token

    workdir: str
        Path to where the plugins folder is.

    daemon: bool
        True if you want to run this as a daemon. False otherwise.

    ping_freq: int
        Frequency of pings to Slack of the bot.
    """
    try:
        setup_bot(token, workdir, ping_freq)
    except:
        log.exception('Error inititalizing RtmBot.')
        sys.exit(1)
    else:
        main_loop(daemon)


def main_loop(daemon):
    def bot_loop():
        try:
            from .rtmbot import BOT
            BOT.start()
        except KeyboardInterrupt:
            raise
        except:
            logging.exception('OOPS')

    if daemon:
        import daemon
        with daemon.DaemonContext():
            bot_loop()
    bot_loop()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--workdir', action='store', dest='workdir',
                        metavar='path', default='.',
                        help='Root path of where the plugins folder is.')
    parser.add_argument('-c', '--config', dest='config', metavar='path',
                        default='slackbot.conf',
                        help='Full path to config file.')
    return parser


def main():
    parser = create_parser()
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as exc:
        logging.exception('Error parsing arguments.')
        parser.error(str(exc))
        sys.exit(1)

    conf_file = args.config
    workdir   = op.abspath(args.workdir)

    #load config file
    config  = yaml.load (file(conf_file, 'r'))
    daemon  = config.get("DAEMON",       False)
    token   = config.get("SLACK_TOKEN",  '')
    pingfrq = config.get("PING_FREQ",    '')

    #logging
    logfile = config.get("LOGFILE", '')
    loglvl  = logging.DEBUG if config.get("DEBUG", True) else logging.INFO
    setup_logging(logfile, loglvl)

    # run
    try:
        log.debug('Starting bot and loading plugins from {}.'.format(workdir))
        start_bot(token, workdir, daemon, pingfrq)
    except KeyboardInterrupt:
        log.exception('Keyboard Interruption')
    except:
        log.exception('Error running slackbot.')
    else:
        sys.exit(0)
    finally:
        sys.exit(1)


if __name__ == "__main__":
    main()
