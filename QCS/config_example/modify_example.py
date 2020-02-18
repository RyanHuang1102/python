#!/usr/bin/python
import ConfigParser
import fcntl
from time import time,sleep
import os
#
MAX_TRY = 20

def FILE_LOCK(path):
    fp = open(path+'.lck','wb')
    TRY = 0
    while(TRY < MAX_TRY):
        try:
            fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except:
            TRY+=1
            print TRY
    if (TRY == MAX_TRY):
        print "Times Out, File Locked"
        return -1
    return fp

def FILE_UNLOCK(fp, path):
    os.unlink(path+'.lck')
    fcntl.flock(fp, fcntl.LOCK_UN)
    return

def Init_Parser(path):
    parser = ConfigParser.SafeConfigParser()
    if (parser.read('test1.cfg') == []):
        open('test1.cfg','wb').close()
    return parser 

fp = FILE_LOCK('test1.cfg')

if (fp == -1):
    exit(1)
else:
    parser = Init_Parser('test1.cfg')
    parser.set('mylun1','dev','/dev/rbd123')
    parser.write(open('test1.cfg','wb'))

FILE_UNLOCK(fp, 'test1.cfg')
