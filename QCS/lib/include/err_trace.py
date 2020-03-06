import logging
import ConfigParser
from logging.handlers import RotatingFileHandler
from lib import *

TRACE_ERROR = 0x0001
TRACE_WARNING = 0x0002
TRACE_ENTRY = 0x0004

#1 Mbytes
def ERR_TRACE(log_path, config_path, trace_flag, string):
    logger = logging.getLogger()
    handler = RotatingFileHandler(log_path, maxBytes = 1024*1024, backupCount = 1)
    formatter = logging.Formatter(fmt = '%(asctime)s %(levelname)s %(message)s', datefmt = '%Y %b %d %a %H:%M:%S')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)

    parser = ConfigParser.SafeConfigParser()
    parser.read(config_path)
    log_flag = parser.get('Global', 'logflags')

    level = trace_flag & int(log_flag)
    if (level == 1):
        logger.setLevel(logging.ERROR)
        logger.error(string)
    elif (level == 2):
        logger.setLevel(logging.WARNING)
        logger.warning(string)
    elif (level == 4):
        logger.setLevel(logging.INFO)
        logger.info(string)
    else:
        return #do nothing
