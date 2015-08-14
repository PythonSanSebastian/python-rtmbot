
import logging

def setup_logging(logfile, level=logging.INFO):
    log_args = {'level'  : level,
                'format' : '%(asctime)s %(message)s'}

    if logfile:
        log_args['filename'] = logfile

    logging.basicConfig(**log_args)
