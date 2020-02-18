#!/usr/bin/python


class haha():
    def __init__(self):
        pass
    def FILE_LOCK(self):
        print "FILE_LOCK"
    def CALL_ME(self):
        self.FILE_LOCK()
        print "CALL_ME"

config=haha()
config.CALL_ME()
