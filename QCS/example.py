#!/usr/bin/python

from qnap_cfg import config
config = config('test1.cfg')
config.setcfg('mylun1', 'dev','/dev/rbd_lun1')
config.setcfg('mylun1', 'alias', 'haha')
config.setcfg('mylun2', 'dev', '/dev/rbd_lun2')

config.rmcfg('mylun1')

config.setcfg('mylun1', 'dev','/dev/rbd_lun1')
config.setcfg('mylun1', 'alias', 'haha')
