#!/usr/bin/python

import logging
from logging.handlers import RotatingFileHandler
#1 Mbytes
class LOG():
    def __init__(self, file_path):
        self.logger = logging.getLogger()
        self.handler = RotatingFileHandler(file_path, maxBytes = 1024*1024, backupCount = 1)
        self.formatter = logging.Formatter(fmt = '%(asctime)s %(levelname)s %(message)s', datefmt = '%a,%d %b,%Y %H:%M:%S')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def CRITICAL_TRACE(self, string):
        self.logger.setLevel(logging.CRITICAL)
        self.logger.info(string)
    def ERROR_TRACE(self, string):
        self.logger.setLevel(logging.ERROR)
        self.logger.info(string)

    def WARNING_TRACE(self, string):
        self.logger.setLevel(logging.WARNING)
        self.logger.info(string)

    def INFO_TRACE(self, string):
        self.logger.setLevel(logging.INFO)
        self.logger.info(string)

    def DEBUG_TRACE(self, string):
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(string)

LOG = LOG('my.log')

a=0
while a<1000:
    LOG.INFO_TRACE("haha"+str(a))
    a+=1
