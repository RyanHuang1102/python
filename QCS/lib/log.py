import logging
from logging.handlers import RotatingFileHandler
from lib import *

TRACE_ERROR = 0x0001
TRACE_WARNING = 0x0002
TRACE_INFO = 0x0004

#1 Mbytes
class LOG():
    def __init__(self, log_path, config_path):
        self.logger = logging.getLogger()
        self.handler = RotatingFileHandler(log_path, maxBytes = 1024*1024, backupCount = 1)
        self.formatter = logging.Formatter(fmt = '%(asctime)s %(levelname)s %(message)s', datefmt = '%Y %b %d %a %H:%M:%S')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

        self.log_flag = config(config_path).Ini_Conf_Get_Field('Global','LogFlags')
        if self.log_flag is -1:
            self.logger.setLevel(logging.ERROR)
            self.logger.error("%s:Can't get LogFlags" %config_path)

    def INFO_TRACE(self, trace_flag, string):
        if self.log_flag is -1:
            return -1

        level = trace_flag & int(self.log_flag)
        if (level == 1):
            self.logger.setLevel(logging.ERROR)
            self.logger.error(string)
        elif (level == 2):
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(string)
        elif (level == 4):
            self.logger.setLevel(logging.INFO)
            self.logger.info(string)
        else:
            return #do nothing
"""
LOG = LOG('my.log','test.cfg')
a=0
while a<40:
    LOG.INFO_TRACE(TRACE_INFO,"haha"+str(a))
    a+=1

LOG.INFO_TRACE(TRACE_ERROR,"123")
"""
