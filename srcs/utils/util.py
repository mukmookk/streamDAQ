import logging
from . from utils.util import config

def reportLog(msg, level):
    """
    msg = message to be logged
    level = level of logging
    """
    log_levels = {
        'debug': logging.debug,
        'info': logging.info,
        'warn': logging.warning, # Note: Use 'warning' instead of 'warn'
        'error': logging.error,
        'critical': logging.critical,
    }

    log_func = log_levels.get(level.lower())

    if log_func is not None:
        log_func(msg)
        print(msg)
    else:
        logging.fatal('Provided log level is not valid')
        print('Provided log level is not valid')