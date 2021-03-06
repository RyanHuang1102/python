#!/usr/bin/python

import logging
from logging.handlers import RotatingFileHandler
TRACE_ERROR = 0x0001
TRACE_WARNING = 0x0002
TRACE_INFO = 0x0004
#1 Mbytes
class LOG():
    def __init__(self, file_path):
        self.logger = logging.getLogger()
        self.handler = RotatingFileHandler(file_path, maxBytes = 1024, backupCount = 1)
        self.formatter = logging.Formatter(fmt = '%(asctime)s %(levelname)s %(message)s', datefmt = '%Y %b %d %a %H:%M:%S')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def INFO_TRACE(self, flag, string):
        value = 3
        level = flag & value
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

LOG = LOG('my.log')

a=0
while a<40:
    LOG.INFO_TRACE(TRACE_INFO,"haha"+str(a))
    a+=1

LOG.INFO_TRACE(TRACE_ERROR,"123")
