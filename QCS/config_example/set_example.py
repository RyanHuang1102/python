#!/usr/bin/python
import ConfigParser
import fcntl
from time import sleep
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
            sleep(0.5)
            print TRY
    if (TRY == MAX_TRY):
        print "Times Out, File Locked"
        return -1
    return fp

def FILE_UNLOCK(fp, path):
    try:
        os.unlink(path+'.lck')
    except:
        pass #unlink fail: it means that file is unlocked.
    fcntl.flock(fp, fcntl.LOCK_UN)
    return

fp = FILE_LOCK('test1.cfg')

if (fp == -1):
    exit(1)
else:
    config_path = 'test1.cfg'
    parser = ConfigParser.SafeConfigParser()
    if (parser.read(config_path) == []):
        parser.add_section('Global')
        parser.set('Global', 'LogFlags', '7') 
        parser.write(open(config_path, 'wb'))

    parser.add_section('mylun1')
    parser.add_section('mylun2')
    parser.set('mylun1','dev','/dev/rbd0')
    parser.set('mylun2','dev','/dev/rbd1')
    parser.write(open('test1.cfg','wb'))
    sleep(10)
    print "done"
#get 
#parser.get(section, field)

FILE_UNLOCK(fp, 'test1.cfg')
